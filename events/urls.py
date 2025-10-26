from django.urls import path
from . import views

urlpatterns = [
    path(' ', views.event, name='event'),
    path('list/', views.event_list, name='event_list'),
    path('<int:id>/', views.event_detail, name='event_detail'),
    path('add/', views.EventForm, name='event_add'),
    path('<int:id>/edit/', views.EventForm, name='event_edit'),
    path('<int:id>/delete/', views.event_delete, name='event_delete'),
    path('create/', views.event_create, name='event_create'),
    path('past/', views.user_events, name='past_events'),
    path('calendar/', views.event_reminder, name='event_calendar'),
    path('search/', views.event_search, name='event_search'),


]
