from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_list, name='booking_list'),
    path('<int:id>/', views.booking_detail, name='booking_detail'),
    path('new/', views.booking_create, name='booking_form'),
    path('<int:id>/edit/', views.booking_edit, name='booking_edit'),
    path('reservations/', views.reservation, name='reservation'),
    path('<int:id>/cancel/', views.booking_cancel, name='booking_cancel'),
    ]
