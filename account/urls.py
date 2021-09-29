from django.urls import path, include
from rest_framework import routers

from .views import *
app_name = 'account'
router = routers.SimpleRouter()
router.register(r'/auth', AuthenticationAPI,basename='auth')
router.register(r'/address', AddressAPI,basename='address')

urlpatterns = [
    path('', include(router.urls), name='auth'),
]
