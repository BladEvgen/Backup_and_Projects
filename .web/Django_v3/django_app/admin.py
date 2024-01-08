from django.contrib import admin
from django_app.models import Package, Product, Review

# Register your models here.
admin.site.register(Package)
admin.site.register(Product)
admin.site.register(Review)