from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginFailed(Exception):
    pass


class RegistrationFailed(Exception):
    pass


class UserDataStructure:
    def __init__(self, first_name=None, last_name=None, email=None, password=None, user_type=0, **kwargs):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = email
        self.password = password
        self.user_type = user_type


class BaseUserModel:
    def __init__(self, request):
        self.request = request

    def logUserIn(self, user_data_structure):
        user = self.getUser(user_data_structure)
        if user:
            login(self.request, user)
        else:
            raise LoginFailed

    @staticmethod
    def register(user_data_structure):
        user = User(**user_data_structure.__dict__)
        user.set_password(user_data_structure.password)
        user.save()
        return user

    @staticmethod
    def getUser(user_data_structure):
        return authenticate(username=user_data_structure.email, password=user_data_structure.password)
