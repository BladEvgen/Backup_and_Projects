from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, MinLengthValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from contracts import utils


class Contragent(models.Model):
    bin = models.CharField(
        max_length=12, validators=[MinLengthValidator(12)], unique=True
    )
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    UserProfile.objects.get_or_create(user=instance)


class Comment(models.Model):
    comment = models.TextField()

    def __str__(self):
        return self.comment


def contract_file_path(instance, filename):
    name, extension = filename.rsplit(".", 1)
    name_transliterated = utils.transliterate(name)
    return f"uploads/userid_{instance.agent_id}/{name_transliterated}.{extension}"


class Contract(models.Model):
    agent = models.ForeignKey(
        Contragent, on_delete=models.CASCADE, related_name="contracts"
    )
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    comment = models.ForeignKey(
        Comment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contracts",
    )
    file = models.FileField(
        upload_to=contract_file_path,
        verbose_name="PDF File",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )

    def __str__(self):
        return f"Contract for {self.agent.title} ({self.date})"
