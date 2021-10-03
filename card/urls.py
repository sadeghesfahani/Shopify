from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r'card', CardAPI, basename='card')
router.register(r'delivery', DeliveryAPI, basename='delivery')
router.register(r'options', OptionsAPI, basename='options')

urlpatterns = [
    path('', include(router.urls), name='card'),
]
