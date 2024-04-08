from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from contracts import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from contracts.swagger import urlpatterns as doc_urls
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path("", views.home, name="home"),
    path("api/contracts/", views.contracts, name="contracts"),
    path("api/agents/", views.agents_detail, name="agents_detail"),
    path("api/agents/<int:id>/", views.agents_detail, name="agents_detail"),
    path("api/user/register/", views.user_register, name="register"),
    path("api/user/details/", views.user_details, name="user_details"),
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
    path("api/token/verify/", TokenVerifyView.as_view()),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/logout/", views.CustomLogoutView.as_view(), name="logout"),
    # path("api/contract/<int:id>", views.contract, name="contract"),
    # path("api/comments/", views.comments, name="comments"),
    # path("api/comment/<int:id>", views.comment, name="comment"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += doc_urls
