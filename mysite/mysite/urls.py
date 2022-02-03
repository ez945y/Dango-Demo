"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, re_path
from restaurants.views import menu, meta, welcome, list_restaurants, comment, login, index, logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu/', menu),
    ##re_path(r'menu/(\d{1,5})', menu),
    path('meta/', meta),
    path('welcome/', welcome),
    path('restaurants_list/', list_restaurants),
    path('index/', index),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', index),
    re_path(r'comment/(\d{1,5})', comment),
]
