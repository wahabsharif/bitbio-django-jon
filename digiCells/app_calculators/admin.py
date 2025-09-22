from django.contrib import admin

# Register your models here.

from .models import CellType, CultureVessel
@admin.register(CellType)
class CellTypeAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'sku', 'recommended_seeding_density')
    search_fields = ('product_name', 'sku')
    list_filter = ('recommended_seeding_density',)
    
@admin.register(CultureVessel)
class CultureVesselAdmin(admin.ModelAdmin):
    list_display = ('plate_format', 'surface_area_cm2', 'media_volume_per_well_ml')
    search_fields = ('plate_format',)
    list_filter = ('surface_area_cm2', 'media_volume_per_well_ml')
