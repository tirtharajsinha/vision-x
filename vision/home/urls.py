from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.index, name="home"),
    path('upload', views.upload, name="upload"),
    path('login', views.loginuser, name="login"),
    path('logout', views.logoutuser, name="logout"),
    path('register', views.register, name="register"),
    path('showimg', views.showimg, name="showimg"),
    path('delimage/<id>', views.delimage, name="delimage"),
    path('profile', views.profile, name="profile"),

]
