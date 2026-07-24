from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('home/', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('help/', views.help_center, name='help_center'),
    path('admin/products/', views.product_list, name='product_list'),
    path('admin/products/create/', views.product_create, name='product_create'),
    path('admin/products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('admin/products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('admin/categories/', views.category_list, name='category_list'),
    path('admin/categories/create/', views.category_create, name='category_create'),
    path('admin/categories/<int:pk>/edit/', views.category_update, name='category_update'),
    path('admin/categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
