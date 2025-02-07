from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), # This is the root path
    path('about/', views.about, name='about'), # This is the about path
    path('contact/', views.contact, name='contact'), # This is the contact path
    path('login/', views.set_login, name='set_login'), # This is the login path
    path('signup/', views.signup, name='signup'), # This is the signup path
    path('logout/', views.logout, name='logout'), # This is the logout path
    path('profile/', views.profile, name='profile'), # This is the profile path
    path('forgot-password/', views.forgot_password, name='forgot-password'), # This is the forgot_password path
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset-password'), # This is the reset_password path

    path('cdashboard/', views.cdashboard, name='cdashboard'), # This is the Home path
]