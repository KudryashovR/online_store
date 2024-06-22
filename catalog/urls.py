from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ContactView, ProductDetailView, ProductCreateView, BlogListView, \
    BlogCreateView, BlogDetailView, BlogUpdateView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('new_product/', ProductCreateView.as_view(), name='new_product'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('blog/new/', BlogCreateView.as_view(), name='new_blog'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<slug:slug>/edit/', BlogUpdateView.as_view(), name='blog_edit')
]
