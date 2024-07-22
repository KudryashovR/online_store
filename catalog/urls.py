from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ContactView, ProductDetailView, ProductCreateView, BlogListView, \
    BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView, ProductUpdateView, ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('new_product/', ProductCreateView.as_view(), name='new_product'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('blog/new/', BlogCreateView.as_view(), name='new_blog'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<slug:slug>/edit/', BlogUpdateView.as_view(), name='blog_edit'),
    path('blog/<slug:slug>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]
