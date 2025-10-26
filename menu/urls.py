from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('<int:pk>/edit/', views.menu_edit, name='menu_edit'),  
    path('<int:pk>/delete/', views.menu_delete, name='menu_delete'),
    path('<int:pk>/', views.menu_detail, name='menu_detail'),
    path('download/', views.menu_download, name='menu_download'),
]
