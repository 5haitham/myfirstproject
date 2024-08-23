# tasks/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.shortcuts import render
from .models import Task  # تأكد من أن هذا السطر صحيح
from .views import user_dashboard

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
   
    path('', views.task_list, name='task_list'),  # مثال على رابط الصفحة الرئيسية
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/new/', views.task_create, name='task_create'),
    path('task/<int:pk>/edit/', views.task_update, name='task_update'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/', views.task_list, name='task_list'),
    path('dashboard/', user_dashboard, name='user_dashboard'),

]





