from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('bulk-rna/', include('bitbio_nucleus_bulk_rna.urls')),
    path('calculators/', include('app_calculators.urls')),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
]
