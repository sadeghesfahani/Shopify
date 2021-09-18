from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Card)
admin.site.register(Order)
admin.site.register(Delivery)
admin.site.register(AdditionalOption)


