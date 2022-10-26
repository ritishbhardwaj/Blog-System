"""Blog_Management_System URL Configuration

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
import imp
from django.contrib import admin
from django.urls import path
from blog import views
from django.conf import settings
from django.conf.urls.static import static

from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('about/', views.about),
    path('contact/', views.contact),
    path('dashboard/<int:id>/', views.Dashboard),
    # path('dashboard/<str:uname>/', views.Dashboard),
    path('signup/', views.user_signup),
    path('login/', views.user_login),
    path('logout/', views.user_logout),
    path('addpost/', views.add_post),
    path('updatepost/<int:id>/', views.update_post),
    path('deletepost/<int:id>/', views.delete_post,name='deletepost'),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]
