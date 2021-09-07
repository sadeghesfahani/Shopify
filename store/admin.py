from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Price)
admin.site.register(Discount)
admin.site.register(Store)