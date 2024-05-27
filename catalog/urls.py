from django.urls import path
from catalog.apps import CatalogConfig

app_name = CatalogConfig.name

urlpatterns = [
    path('', name='home'),
    path('contacts/', name='contacts'),
]