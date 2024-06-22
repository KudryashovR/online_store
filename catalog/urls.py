from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import new_product, ProductListView, ContactView, ProductDetailView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('new_product/', new_product, name='new_product'),
]
