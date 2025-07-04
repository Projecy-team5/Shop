from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('admin/orders/', views.admin_order_list, name='admin_order_list'),
    path('admin/orders/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin/orders/<int:order_id>/update-status/', views.admin_order_update_status, name='admin_order_update_status'),
    path('admin/products/', views.admin_product_list, name='admin_product_list'),
    path('admin/product/', views.admin_product, name='admin_product'),
    path('admin/products/add/', views.add_product, name='add_product'),
    path('admin/products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('admin/products/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('admin/users/', views.admin_user_list, name='admin_user_list'),
    path('admin/users/edit/<int:pk>/', views.admin_user_edit, name='admin_user_edit'),
    path('admin/users/delete/<int:pk>/', views.admin_user_delete, name='admin_user_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)