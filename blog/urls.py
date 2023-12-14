"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

from django.urls import path
from blogapp import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile_tmp, name='profile_tmp'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
    path('main/', views.main_view, name="main"),
    path('', views.main_view, name="main"),
    path('low_auth/<str:reason>/', views.low_auth, name='low_auth'),
    path('upload/', views.upload, name='upload'),
    path('page/<int:id>/', views.page_view, name='page'),
    path('all/', views.all_pages, name='all'),
    path("blog_update/<int:blog_id>/", views.blog_update,name="blog_update"),
    path("blog_delete/<int:blog_id>/", views.blog_delete,name="blog_delete"),
    path("user_update/",views.user_update,name="user_update")
]