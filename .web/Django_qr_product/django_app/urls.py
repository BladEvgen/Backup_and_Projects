from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django_app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("create/", views.create_wine, name="create_wine"),
    path("wine/<int:wine_id>/", views.wine_detail, name="wine_detail"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("wine/<int:wine_id>/", views.wine_detail, name="wine_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
