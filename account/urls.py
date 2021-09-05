from django.urls import path
from .views import *
app_name = 'account'
urlpatterns = [
    path('/signup/', AuthenticationView.as_view(), name='authentication'),
    path('/checkuserexistence', CheckUsernameExistence, name='checkuserexistance'),
    path('/generalinfo', GeneralInfo.as_view(), name='generalinfo'),
]
