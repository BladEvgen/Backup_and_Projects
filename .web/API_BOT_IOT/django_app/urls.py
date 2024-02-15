from django.urls import path
from . import views

urlpatterns = [
    path("get_params/", views.get_params_api, name="get-params"),
    path("sent_messages/", views.sent_message_api, name="sent-messages"),
    path("api", views.api, name="api"),
    path("", views.home, name="home"),
]
