from django.db import models


# Create your models here.
class Products(models.Model):
    month = models.DateField()
    shop = models.CharField(max_length=100)
    count = models.IntegerField()
    price = models.IntegerField()
    category = models.CharField(max_length=100)

    def __str__(_self):
        return _self.shop
