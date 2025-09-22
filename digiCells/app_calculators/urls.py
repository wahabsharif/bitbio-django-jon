from django.urls import path
from . import views

app_name = 'calculators'

urlpatterns = [
    path('', views.calculators_list, name='calculators_list'),
    path('seeding/', views.cell_seeding_calculator_view, name='cell_seeding_calculator'),
]

