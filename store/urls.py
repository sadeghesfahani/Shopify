from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.SimpleRouter()
router.register(r'product', ProductAPI,basename='product')
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category', CategoryApi.as_view(), name='categories'),
    path('category/<int:category_id>', CategoryApi.as_view(), name='category'),
    path('store/<int:store_id>', StoreApi.as_view(), name='category'),
    path('store', StoreApi.as_view(), name='category'),
    path('menu', MenuApi.as_view(), name='menu'),
    path('', include(router.urls), name='product'),

]
