from django.urls import path
from . import views

urlpatterns = [
    path('', views.log_reg),
    path('login', views.login),
    path('register', views.register),
    path('mybottleshop', views.profile),
    path('logout', views.logout),
 ]