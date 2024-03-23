from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class UserExtend(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.user.is_active = self.is_active
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.user.username} - {'Разблокирован' if self.is_active else 'Забанен'}"
        )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    UserExtend.objects.get_or_create(user=instance)


class FailedLoginAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=45)
    timestamp = models.DateTimeField(auto_now_add=True)


class AccountLock(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    release_at = models.DateTimeField()
