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
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views
import django.contrib.auth.views
from django.urls import path, re_path, include
import restaurants.views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu/', restaurants.views.menu),
    #re_path(r'menu/(\d{1,5})', restaurants.views.menu),
    re_path(r'menu/(?P<pk>\d+)', restaurants.views.MenuView.as_view()),
    path('meta/', restaurants.views.meta),
    path('welcome/', restaurants.views.welcome),
    path('index/', TemplateView.as_view(template_name='index.html')),
    path('accounts/login/', django.contrib.auth.views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', TemplateView.as_view(template_name='index.html')),
    path('accounts/register/', restaurants.views.register),
    #re_path(r'comment/(?P<id>\d{1,5})', restaurants.views.comment),
    re_path(r'comment/(?P<pk>\d+)', restaurants.views.CommentView.as_view()),
    path('firstmenu/', restaurants.views.menu),
    path('restaurants_list/', django.contrib.auth.views.login_required(
        restaurants.views.RestaurantsView.as_view(), {'model': restaurants.models.Restaurant})),
    path('users_list/', restaurants.views.list,
         {'model': django.contrib.auth.models.User}),
    path('test/', restaurants.views.test),
    path(r'', TemplateView.as_view(template_name='index.html')),
]
if settings.DEBUG:
    urlpatterns += [
        path('test/', restaurants.views.test),
    ]
    """path('restaurants_list/', django.contrib.auth.views.login_required(
        restaurants.views.list, {'model': restaurants.models.Restaurant}))"""
    """path('restaurants_list/', restaurants.views.list,
            {'model': restaurants.models.Restaurant}),"""

