from django.urls import path
from django_app import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("settings/get/", views.settings_get, name="settings_get"),
    path("settings/set/", views.settings_set),
    path("settings/change/", views.settings_change, name="settings_change"),
]
