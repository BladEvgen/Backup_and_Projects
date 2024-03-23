import uuid

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django_app.models import Token, UserExtend
from django_app.utils import (
    auth_required,
    check_login_attempts,
    delete_expired_failed_login_attempts,
    is_account_locked,
    lock_account,
    log_failed_login_attempt,
    password_check,
    username_check,
)

"""
{
"username": "Evgen_3",
"password": "Qwertyu123!"    
    
}
"""


@csrf_exempt
@api_view(http_method_names=["POST"])
def token(request):
    username = request.data.get("username", None)
    password = request.data.get("password", None)
    ip_address = request.META.get("REMOTE_ADDR", None)

    if not password_check(password) or not username_check(username):
        return Response(data={"error": "Invalid"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        user = User.objects.get(username=username)
        if is_account_locked(user):
            Token.objects.filter(user=user).delete()
            return Response(
                data={"error": "Account locked, try again later."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if user.check_password(password):
            token = "".join(str(uuid.uuid4()) for _ in range(4))
            Token.objects.create(user=user, token=token)

            delete_expired_failed_login_attempts()

            return Response(data={"token": token})
        else:
            log_failed_login_attempt(user, ip_address)

            if check_login_attempts(user, ip_address):
                lock_account(user)
                Token.objects.filter(user=user).delete()
                return Response(
                    data={"error": "Account locked, try again later."},
                    status=status.HTTP_403_FORBIDDEN,
                )

    except User.DoesNotExist:
        pass

    return Response(
        data={"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(http_method_names=["GET"])
@auth_required
def user_list(request):
    users = UserExtend.objects.all()
    data = [{"username": user.username} for user in users]
    return Response(data={"data": data})


@api_view(http_method_names=["POST"])
def token_block(request):
    token_to_block_str = request.data.get("token", "")
    try:
        token = Token.objects.get(token=token_to_block_str)
        token.delete()
        return Response(
            data={"data": "Successfully deleted"}, status=status.HTTP_200_OK
        )
    except Token.DoesNotExist:
        return Response(
            data={"error": "Token not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(http_method_names=["GET"])
@auth_required
def token_verify(request):
    return Response(data={"data": "Success verified"}, status=status.HTTP_200_OK)
