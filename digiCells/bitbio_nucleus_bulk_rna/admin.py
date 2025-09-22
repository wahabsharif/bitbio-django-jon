from django.contrib import admin

# Register your models here.
from .models import *


# Register your models here.
admin.site.register(AnalysisOutput)
admin.site.register(GeneCollection)
admin.site.register(Gene)
admin.site.register(Tier)
admin.site.register(UserTier)
admin.site.register(UserGeneRequest)

