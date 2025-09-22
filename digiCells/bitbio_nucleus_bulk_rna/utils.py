from .models import Gene, UserGeneRequest, UserTier, Tier
from django.db import transaction


def convert_id_list_to_obj(gene_id_list):
    """
    Converts a list of gene identifiers into a list of Gene model objects.

    Each identifier in `gene_id_list` should be a string formatted as "gene_name_ensembl_id"
    (e.g., "ENSG00000141510_TP53"). The function splits each identifier to extract the
    `gene_name` and `ensembl_id`, then attempts to retrieve the corresponding `Gene` object
    from the database. If a matching `Gene` object is found, it is added to the result list.
    If no matching object is found or multiple objects are found, an error message is printed.

    Parameters:
        gene_id_list (list of str): A list of gene identifiers, each formatted as "ensembl_id_gene_name".

    Returns:
        list of Gene: A list of `Gene` model instances corresponding to the given identifiers.
                      Only genes that match uniquely in the database are included.

    Exceptions:
        - Prints "No gene found with the specified criteria." if no `Gene` object matches a given identifier.
        - Prints "Multiple genes found with the specified criteria." if more than one `Gene` object matches a given identifier.

    Example:
        gene_id_list = ["ENSG00000141510_TP53", "ENSG00000012048_BRCA1"]
        selected_genes = convert_id_list_to_obj(gene_id_list)
        # selected_genes will be a list of `Gene` objects corresponding to TP53 and BRCA1.
    """

    selected_gene_objects = []
    for a_gene in gene_id_list:
        ensembl_id, gene_name = a_gene.split("_", 1)
        print(ensembl_id, gene_name)
        try:
            selected_gene_objects.append(Gene.objects.get(gene_name=gene_name))
        except Gene.DoesNotExist:
            print("No gene found with the specified criteria.")
        except Gene.MultipleObjectsReturned:

            check_list = []

            for a_gene_object in Gene.objects.filter(gene_name=gene_name):
                print(a_gene_object.df_string.split("_")[0], ensembl_id)
                if a_gene_object.df_string.split("_")[0] == ensembl_id:
                    check_list.append(a_gene_object)

            if len(check_list) > 1:
                print("Multiple genes found with the specified criteria.")
                print(Gene.objects.filter(gene_name=gene_name))
                raise Exception("Multiple genes found with the specified criteria.")
            else:
                selected_gene_objects.append(check_list[0])

    return selected_gene_objects


def find_genes_in_collection(user_genes, gene_collection):
    """
    Checks which genes in a user-provided list of Gene objects are present in a given GeneCollection.

    Parameters:
        user_genes (list of Gene): A list of Gene objects to check.
        gene_collection (GeneCollection): The GeneCollection object against which to check for membership.

    Returns:
        tuple: A tuple containing two lists:
               - The first list contains genes from user_genes found in gene_collection.
               - The second list contains genes from user_genes not found in gene_collection.
    """
    # Convert the collection's included_genes queryset to a set of IDs for quick lookup
    collection_gene_ids = set(gene_collection.included_genes.values_list('id', flat=True))

    # Separate the user genes into found and not found lists
    found_genes = []
    not_found_genes = []

    for gene in user_genes:
        if gene.id in collection_gene_ids:
            found_genes.append(gene)
        else:
            not_found_genes.append(gene)

    return found_genes, not_found_genes


def record_user_gene_request(accessed_user_genes):
    pass


def center_data(df):
    """Centers the data by subtracting the mean of each row (gene)."""
    return df.sub(df.mean(axis=1), axis=0)


def scale_data(df):
    """Scales the data by dividing each row by its standard deviation."""
    return df.div(df.std(axis=1), axis=0)


def center_and_scale_data(df):
    """Centers and scales the data (z-score normalization) for each row (gene)."""
    centered = df.sub(df.mean(axis=1), axis=0)
    return centered.div(centered.std(axis=1), axis=0)


def transform_tpm_data(df, center=False, scale=False, replace_nan=True):
    """
    Transforms the data based on the specified options:
    - center: if True, centers the data.
    - scale: if True, scales the data.
    - both: if both center and scale are True, performs z-score normalization.
    - replace_nan: if True, replaces NaN values with 0.0 after transformations.

    Returns the transformed DataFrame.
    """
    # Apply transformations based on options
    if center and scale:
        df = center_and_scale_data(df)
    elif center:
        df = center_data(df)
    elif scale:
        df = scale_data(df)

    # Replace NaN values with 0.0 if replace_nan is True
    if replace_nan:
        df = df.fillna(0.0)

    return df



def update_user_gene_request(user, new_genes):
    """
    Updates the UserGeneRequest for a given user with new genes.

    Args:
        user (User): The user whose gene request will be updated.
        new_genes (list): A list of Gene objects to add to the user's request.

    Returns:
        tuple: (added_genes, skipped_genes)
            - added_genes: A list of Gene objects that were successfully added.
            - skipped_genes: A list of Gene objects that were already in the request.
    """
    try:
        # Retrieve or create the UserGeneRequest object
        user_request, created = UserGeneRequest.objects.get_or_create(user=user)

        # Get the set of genes already in the request
        existing_genes = set(user_request.genes.all())

        # Separate new genes into those to add and those to skip
        added_genes = []
        skipped_genes = []

        for gene in new_genes:
            if gene not in existing_genes:
                added_genes.append(gene)
            else:
                skipped_genes.append(gene)

        # Add the new genes to the UserGeneRequest
        with transaction.atomic():  # Ensure atomicity
            user_request.genes.add(*added_genes)

        return added_genes, skipped_genes

    except Exception as e:
        # Handle exceptions and optionally log the error
        print(f"Error updating user gene request: {e}")
        return [], []


def get_or_create_user_tier_and_request(user):
    """
    Ensure the user has a UserTier and UserGeneRequest object.
    Automatically assign the 'Free' tier if the user has no tier.

    Args:
        user (User): The user object.

    Returns:
        tuple: (UserTier, UserGeneRequest, usage_percentage)
    """
    try:
        # Get the user's tier and gene request
        user_tier = UserTier.objects.get(user=user)
    except UserTier.DoesNotExist:
        # Assign the user to the default 'Free' tier if they don't have one
        free_tier, _ = Tier.objects.get_or_create(name="Free", defaults={"max_genes": 100})
        user_tier = UserTier.objects.create(user=user, tier=free_tier)

    try:
        # Get the user's gene request object
        user_request = UserGeneRequest.objects.get(user=user)
    except UserGeneRequest.DoesNotExist:
        # Create a new UserGeneRequest for the user if it doesn't exist
        user_request = UserGeneRequest.objects.create(user=user)

    # Calculate usage percentage
    usage_percentage = (user_request.genes.count() / user_tier.tier.max_genes) * 100

    return user_tier, user_request, usage_percentage