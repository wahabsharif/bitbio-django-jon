from django import forms
from .models import CellType, CultureVessel

class SeedingCalculatorForm(forms.Form):
    suspension_volume = forms.FloatField(label="Cell stock volume (mL)", min_value=0.01, initial=1.0)
    count1 = forms.FloatField(label="Live cell count 1 (x10⁶ cells/mL)", min_value=0.01)
    count2 = forms.FloatField(label="Live cell count 2 (x10⁶ cells/mL)", required=False)
    count3 = forms.FloatField(label="Live cell count 3 (x10⁶ cells/mL)", required=False)

    viability1 = forms.FloatField(label="Viability 1 (%)", min_value=0, max_value=100, initial=100)
    viability2 = forms.FloatField(label="Viability 2 (%)", required=False)
    viability3 = forms.FloatField(label="Viability 3 (%)", required=False)

    cell_type = forms.ModelChoiceField(queryset=CellType.objects.all(), required=False)
    seeding_density = forms.FloatField(label="Seeding density (cells/cm²)", min_value=0)

    culture_vessel = forms.ModelChoiceField(queryset=CultureVessel.objects.all(), required=False)
    surface_area = forms.FloatField(label="Surface area (cm²/well)", min_value=0.01)
    media_volume = forms.FloatField(label="Media volume (mL/well)", min_value=0.01)

    num_wells = forms.IntegerField(label="Number of wells", min_value=1, initial=96)
    buffer = forms.FloatField(label="Dead volume allowance (%)", min_value=0, initial=10.0)


