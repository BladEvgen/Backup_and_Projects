from django.contrib import admin
from .models import Winery, Wine, WineReview, WineCategory

# Register your models here.
admin.site.register(Wine)
admin.site.register(Winery)
admin.site.register(WineReview)
admin.site.register(WineCategory)
