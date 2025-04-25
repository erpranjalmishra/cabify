
from django.contrib import admin
from django.urls import path
from Mainapp.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homepage,name="home"),
    path("login/",loginpage,name="login"),
    path("register/",register,name="register"),
    path('profile/',profile, name='profile'),
    path('admindashboard/',admin_dashboard, name='admin_dashboard'),
]
