from django.urls import path
from . import views
from .views import ProductSearchView

urlpatterns = [
    # Category URLs
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('categories/<int:pk>/products/', views.CategoryProducts.as_view(), name='category-products'),
    
    # Product URLs
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    path('products/<int:pk>/images/', views.ProductImages.as_view(), name='product-images'),
    
    # Consignment URLs
    path('consignments/', views.ConsignmentList.as_view(), name='consignment-list'),
    path('consignments/<int:pk>/', views.ConsignmentDetail.as_view(), name='consignment-detail'),
    path('consignments/<int:pk>/status/', views.ConsignmentStatus.as_view(), name='consignment-status'),
    
    # Search URL
    path('search/', ProductSearchView.as_view(), name='product-search'),
] 