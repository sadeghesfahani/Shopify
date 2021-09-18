from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from account.models import Address
from shopify_first_try.utils import getObject
from store.errors import handleError

User = get_user_model()


class LoginFailed(Exception):
    pass


class RegistrationFailed(Exception):
    pass


class UserDataStructure:
    def __init__(self, first_name=None, last_name=None, email=None, password=None, user_type=0, *args, **kwargs):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = email
        self.password = password
        self.user_type = user_type


class BaseUserModel:
    def __init__(self, request=None):
        self.request = request

    def logUserInByInfo(self, user_data_structure):
        user = self.getUser(user_data_structure)
        if user:
            login(self.request, user)
        else:
            raise LoginFailed

    def logUserInByInstance(self, user):
        login(self.request, user)

    @staticmethod
    def register(user_data_structure):
        user = User(**user_data_structure.__dict__)
        user.set_password(user_data_structure.password)
        user.save()
        return user

    @staticmethod
    def getToken(user):
        token, created = Token.objects.get_or_create(user=user)
        return token.key

    @staticmethod
    def getUser(user_data_structure):
        return authenticate(username=user_data_structure.email, password=user_data_structure.password)

    @staticmethod
    @handleError(User)
    def getUserByToken(token):
        return User.objects.get(auth_token=token)

    @staticmethod
    @handleError(User)
    def getUserById(user_id):
        return User.objects.get(pk=user_id)

    @handleError(User)
    def addAddress(self, user, postal_code, address):
        user_object = getObject(User, user)
        newly_added_address = Address(user=user_object, address=address, postal_code=postal_code)
        newly_added_address.save()
        return newly_added_address
