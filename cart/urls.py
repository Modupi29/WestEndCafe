from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:item_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:item_id>/', views.cart_delete, name='cart_delete'),
    path('update/<int:item_id>/', views.cart_update, name='cart_update'),  # <- add this
    path('checkout/', views.checkout, name='cart_checkout'),
    path('success/', views.order_success, name='order_success'),
    path('clear/', views.clear_cart, name='clear_cart'),
    path('pay-now/', views.pay_now, name='pay_now'),
    path('pay-later/', views.pay_later, name='pay_later'),
]
