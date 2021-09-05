from django.urls import path
from .views import *
app_name = 'account'
urlpatterns = [
    path('/signup/', RegisterView.as_view(), name='register'),
    path('/checkuserexistence', CheckUsernameExistence, name='checkuserexistance'),
    path('/generalinfo', GeneralInfo.as_view(), name='generalinfo'),
]
