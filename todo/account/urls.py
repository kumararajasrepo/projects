from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("signin", views.signin, name="url-signin"),
    path("signup", views.signup, name="url-signup"),
    path("signout", views.signout, name="url-signout"),
]
