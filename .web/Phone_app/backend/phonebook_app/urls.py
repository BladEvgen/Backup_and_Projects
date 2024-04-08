from django.urls import path
from phonebook_app import views

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "api/get_person_info/",
        views.get_person_info,
        name="get_person_info",
    ),
    path(
        "api/get_person_info/<int:person_id>/",
        views.get_person_info,
        name="get_person_info",
    ),
    path("get_person_info/", views.get_person_info_jinja),
]
