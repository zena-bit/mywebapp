from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('remove-one/<int:product_id>/', views.remove_one_from_cart, name='remove_one_from_cart'),
    path('update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('mpesa/token/', views.get_access_token_view, name='mpesa-token'),
    path('payment/<int:order_id>/', views.initiate_payment_page, name='initiate_payment_page'),
    path('payment/<int:order_id>/initiate/', views.initiate_payment, name='initiate_payment'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa-callback'),
]

