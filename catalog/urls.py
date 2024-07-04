from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ContactView, ProductDetailView, ProductCreateView, BlogListView, \
    BlogCreateView, BlogDetailView, BlogUpdateView, BlogDeleteView, ProductUpdateView, ProductDeleteView, \
    VersionCreateView, VersionUpdateView, VersionDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('new_product/', ProductCreateView.as_view(), name='new_product'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('blog/new/', BlogCreateView.as_view(), name='new_blog'),
    path('blog/<slug:slug>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<slug:slug>/edit/', BlogUpdateView.as_view(), name='blog_edit'),
    path('blog/<slug:slug>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('versions/new/', VersionCreateView.as_view(), name='version_create'),
    path('versions/<int:pk>/edit/', VersionUpdateView.as_view(), name='version_update'),
    path('versions/<int:pk>/delete/', VersionDeleteView.as_view(), name='version_delete'),
]
