from django import template

register = template.Library()


# For improved filtering on group association in templates
@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

# Extract df_string values from a list of Gene objects
@register.filter(name='extract_df_strings')
def extract_df_strings(gene_list):
    """
    Extracts df_string property values from each Gene object in the provided list.
    This is used to convert a list of Gene objects into a list of strings in the format 'ensembl_id_gene_name'
    for use in templates.
    
    Args:
        gene_list: List of Gene model objects
    
    Returns:
        List of strings, each in the format 'ensembl_id_gene_name'
    """
    return [gene.df_string for gene in gene_list] if gene_list else []


