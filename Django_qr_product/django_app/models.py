from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# TODO дату добавления и исхода менять изменяя от региона для view template и models MVT


class Winery(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.location}"


class WineCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"


class Wine(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    production_date = models.DateField()
    expiration_date = models.DateField()
    winery = models.ForeignKey(Winery, on_delete=models.CASCADE)
    category = models.ForeignKey(
        WineCategory, on_delete=models.CASCADE, null=True, blank=True
    )
    picture = models.ImageField(
        upload_to="wine_images/",
        null=True,
        blank=True,
        default=None,
        editable=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "webp"])
        ],
    )
    qr_code = models.ImageField(
        upload_to="qr_codes/",
        null=True,
        blank=True,
        default=None,
        editable=True,
        validators=[FileExtensionValidator(allowed_extensions=["png"])],
    )

    def is_expired(self):
        return self.expiration_date < timezone.now().date()

    def get_absolute_url(self):
        return reverse("wine_detail", args=[str(self.id)])

    def __str__(self):
        return f"{self.name} ({self.winery.name})"


class WineReview(models.Model):
    wine = models.ForeignKey(Wine, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.author.username} - {self.wine.name} - Rating: {self.rating}"
