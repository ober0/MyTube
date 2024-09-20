from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('password-reset/', views.password_reset, name='password-reset'),
    path('register/email-success/', views.email_success, name='email-success'),
    path('register/verified/', views.register_verified),
]
