import re

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from .models import AccountLock, FailedLoginAttempt, Token, UserExtend


def log_failed_login_attempt(user, ip_address):
    FailedLoginAttempt.objects.create(user=user, ip_address=ip_address)


def check_login_attempts(user, ip_address):
    twenty_minutes_ago = timezone.now() - timezone.timedelta(minutes=20)
    failed_attempts = FailedLoginAttempt.objects.filter(
        user=user, ip_address=ip_address, timestamp__gte=twenty_minutes_ago
    ).count()

    return failed_attempts >= 10


def lock_account(user):
    release_at = timezone.now() + timezone.timedelta(minutes=10)
    delete_expired_account_locks()
    AccountLock.objects.update_or_create(user=user, defaults={"release_at": release_at})
    user.is_active = False
    user.save()


@receiver(post_save, sender=UserExtend)
def update_user_status(sender, instance, **kwargs):
    if instance.user.is_active != instance.is_active:
        instance.user.is_active = instance.is_active
        instance.user.save()


def delete_expired_failed_login_attempts():
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    expired_attempts = FailedLoginAttempt.objects.filter(timestamp__lt=thirty_days_ago)
    expired_attempts.delete()


def delete_expired_account_locks():
    now = timezone.now()
    expired_locks = AccountLock.objects.filter(release_at__lte=now)
    for lock in expired_locks:
        if lock.user.is_active is False:
            lock.user.is_active = True
            lock.user.save()
        lock.delete()


def is_account_locked(user):
    delete_expired_account_locks()
    try:
        lock = AccountLock.objects.get(user=user)
        if lock.release_at > timezone.now():
            return True
        else:
            lock.delete()
            return False
    except AccountLock.DoesNotExist:
        return False


def password_check(password: str) -> bool:
    return (
        True
        if re.match(
            r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-_]).{10,}$",
            password,
        )
        is not None
        else False
    )


def username_check(username: str) -> bool:
    return (
        True
        if re.match(r"^(?=.*?[A-Za-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-_]).{4,}$", username)
        is not None
        else False
    )


def auth_required(func):
    def wrapper(request, *args, **kwargs):
        token_str = request.query_params.get("token", "") or request.data.get(
            "token", ""
        )
        if not token_str:
            return Response(
                data={"error": "Token not provided"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            token = Token.objects.get(token=token_str)
        except Token.DoesNotExist:
            return Response(
                data={"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
            )

        if token.is_expired():
            return Response(
                data={"error": "Token expired"}, status=status.HTTP_401_UNAUTHORIZED
            )

        request.user = token.user
        return func(request, *args, **kwargs)

    return wrapper
