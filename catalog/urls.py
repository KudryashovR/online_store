from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contacts, product_detail, new_product

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('new_product/', new_product, name='new_product'),
]
