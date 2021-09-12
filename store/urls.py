from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r'product', ProductAPI,basename='product')
urlpatterns = [
    path('', include(router.urls), name='product'),
]
