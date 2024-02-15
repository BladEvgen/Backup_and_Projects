from django.db import models
from django.utils import timezone


class Device(models.Model):
    device_id = models.CharField(max_length=255, unique=True)


class DeviceData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()
    is_working = models.BooleanField()
    fuel = models.IntegerField()
    speed = models.IntegerField()
    device_time = models.DateTimeField()
    server_time = models.DateTimeField(default=timezone.now)
