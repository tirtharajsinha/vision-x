
from django.contrib import admin
from django.urls import path,include
from home import views
urlpatterns = [
    
    path('',views.index,name="home"),
    path('login',views.loginuser,name="login"),
    path('logout',views.logoutuser,name="logout"),
    path("about",views.about,name="about"),
    path("services",views.services,name="services"),
    path("contact",views.contact,name="contact"),
    path("portfolio",views.portfolio,name="portfolio"),
    path("register",views.register,name="register"),
    path("profile",views.profile,name="profile"),
    path("del_user",views.del_user,name="del_user"),

]
