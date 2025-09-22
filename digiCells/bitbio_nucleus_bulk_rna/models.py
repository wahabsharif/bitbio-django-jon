from django.db import models
from django.contrib.auth.models import User, Group


class AnalysisOutput(models.Model):

    ANALYSIS_TYPE_CHOICES = [
        ('bulk_rna', 'Bulk RNA'),
        # Add other analysis types here if needed
    ]

    analysis_type = models.CharField(
        max_length=50,
        choices=ANALYSIS_TYPE_CHOICES,
        default='bulk_rna'
    )
    project = models.TextField(null=True, blank=True)
    product = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    conditions = models.TextField(null=True, blank=True)
    added_by = models.TextField(null=True, blank=True)
    origin = models.TextField(null=True, blank=True)
    linked_benchling_entry = models.CharField(max_length=255, null=True, blank=True)  # Assuming Benchling entry is referenced via an ID or URL
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_visible_in_commercial_app = models.BooleanField(default=False)
    metadata = models.JSONField()
    file_path = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_analysis_type_display()} Analysis - {self.created_at}"


class Gene(models.Model):
    gene_name = models.CharField(max_length=100)
    ensembl_id = models.CharField(max_length=100)
    long_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.gene_name} ({self.ensembl_id})"

    def get_base_ensembl_id(self):
        """Returns the base Ensembl ID without the version suffix."""
        return self.ensembl_id.split('.')[0]

    @property
    def df_string(self):
        """Returns a string in the format ensembl_id_gene_name."""
        return f"{self.ensembl_id.split('.')[0]}_{self.gene_name}"


class GeneCollection(models.Model):
    collection_name = models.CharField(max_length=100)
    linked_analyses = models.ManyToManyField(AnalysisOutput, blank=True)
    description = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    included_genes = models.ManyToManyField(Gene, blank=True)
    # Private dataset, available only for the user that created it
    private_collection = models.BooleanField(default=True)
    # Internal collection or commercial?
    customer_visible = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.collection_name}"


class Tier(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)  # Optional field for tier details
    max_genes = models.PositiveIntegerField(default=100)  # Gene limit for the tier

    def __str__(self):
        return f"{self.name} (Limit: {self.max_genes})"


class UserTier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)  # Link to the Tier model

    def __str__(self):
        return f"{self.user.username} - {self.tier.name}"


class UserGeneRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genes = models.ManyToManyField(Gene, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_within_limit(self):
        """
        Check if the number of requested genes is within the user's tier limit.
        """
        try:
            user_tier = UserTier.objects.get(user=self.user)
            return self.genes.count() <= user_tier.tier.max_genes
        except UserTier.DoesNotExist:
            return False  # Handle case where the user has no assigned tier

