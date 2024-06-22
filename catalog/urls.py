from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import product_detail, new_product, ProductListView, ContactView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('new_product/', new_product, name='new_product'),
]
