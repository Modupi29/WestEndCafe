from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('accounts/sign-up/',views.user_registration_view, name='sign-up'),
    path('accounts/account-activation/<str:uidb64>/<str:token>/', views.account_activation_view, name='account-activation'),
    path('login/', views.login_view, name='dologin'),
    path('logout/', views.logout_view, name='dologout'),
    path('dashboard/', views.index_view, name='dashboard'),
    path('dashboard/', views.index_view, name='dashboard'),
    path('admin-dashboard/', views.admin_home_view, name='admin-dashboard'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('profile/', views.profile_view, name='profile'),
    path('help/', views.help_view, name='help'),
    path('refund/', views.refund_view, name='refund'),

]
