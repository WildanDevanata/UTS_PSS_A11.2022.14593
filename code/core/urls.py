from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'admins', views.AdminViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'suppliers', views.SupplierViewSet)
router.register(r'items', views.ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Additional API endpoints
    path('reports/stock-summary/', views.stock_summary, name='stock-summary'),
    path('reports/low-stock/', views.low_stock_items, name='low-stock-items'),
    path('reports/category/<int:category_id>/items/', views.items_by_category, name='items-by-category'),
    path('reports/categories/items/', views.items_by_category, name='all-categories-items'),
    path('reports/categories/summary/', views.category_summary, name='category-summary'),
    path('reports/suppliers/summary/', views.supplier_summary, name='supplier-summary'),
    path('reports/system/summary/', views.system_summary, name='system-summary'),
]