from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:id>/', views.order_detail, name='order_detail'),
    path('success/', views.order_success, name='order_success'),
    path('<int:id>/complete/', views.order_complete, name='order_complete'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('<int:id>/edit/', views.OrderItem, name='order_edit'),
    path('delete/<int:order_id>/', views.order_delete, name='order_delete'),
]