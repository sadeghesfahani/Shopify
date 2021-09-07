from django.urls import path
from .views import *
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('categories', HomeApi.as_view(), name='categories'),
    path('category/<int:category_id>', CategoryApi.as_view(), name='category'),

]
