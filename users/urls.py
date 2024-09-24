from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('password-reset/', views.password_reset, name='password-reset'),
    path('password-reset/verified/', views.password_reset_verified, name='password-reset-verified'),
    path('register/email-success/', views.email_success, name='email-success'),
    path('register/verified/', views.register_verified, name='register-verified'),
    path('logout/', views.exit, name='exit'),
    path('<int:id>/', views.profile, name='profile')
]
