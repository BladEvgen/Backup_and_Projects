from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    is_visible = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name



class Package(models.Model):
    weight = models.FloatField()
    date_of_receipt = models.DateTimeField()
    date_of_dispatch = models.DateTimeField(null=True, blank=True)
    price = models.FloatField()

    recipient_first_name = models.CharField(max_length=50)
    recipient_last_name = models.CharField(max_length=50)
    recipient_phone_number = models.CharField(max_length=20)
    recipient_address = models.CharField(max_length=255)

    sender_first_name = models.CharField(max_length=50)
    sender_last_name = models.CharField(max_length=50)

    def __str__(self):
        return (
            f"Package(id={self.id}, weight={self.weight}, date_of_receipt={self.date_of_receipt}, "
            f"date_of_dispatch={self.date_of_dispatch}, price={self.price}, "
            f"recipient={self.recipient_first_name} {self.recipient_last_name}, "
            f"sender={self.sender_first_name} {self.sender_last_name})"
        )
