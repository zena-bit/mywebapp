from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/dashboard/', views.my_dashboard, name='my_dashboard'),
    path('accounts/orders/', views.my_orders, name='my_orders'),
    path('accounts/orders/<str:order_code>/', views.order_detail, name='order_detail'),
    path('accounts/coupons/', views.my_coupons, name='my_coupons'),
    path('accounts/wishlist/', views.my_wishlist, name='my_wishlist'),
    path('accounts/wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('accounts/wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]
