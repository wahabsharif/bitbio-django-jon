from django.db import models

class CellType(models.Model):
    product_name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, blank=True, null=True)
    recommended_seeding_density = models.PositiveIntegerField(help_text="Cells per cm²")

    def __str__(self):
        return f"{self.product_name} ({self.sku})" if self.sku else self.product_name

class CultureVessel(models.Model):
    plate_format = models.CharField(max_length=100)
    surface_area_cm2 = models.FloatField(null=True, blank=True)
    media_volume_per_well_ml = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.plate_format

