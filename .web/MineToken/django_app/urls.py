from django.urls import path
from django_app import views

urlpatterns = [
    path("token/", views.token),
    path("token/check/", views.token_verify),
    path("user/list/", views.user_list),
    #! если пользоваетль пытется зайти с заблокированного токена пишется лог
    path("token/block/", views.token_block),
]
