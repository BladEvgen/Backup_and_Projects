from django.contrib import admin
from django.urls import path, include
from django_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("django_app.urls")),
    path("api-auth/", include("rest_framework.urls")),
]
