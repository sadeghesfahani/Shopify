from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r'card', CardAPI, basename='card')

urlpatterns = [
    path('', include(router.urls), name='card'),
]
