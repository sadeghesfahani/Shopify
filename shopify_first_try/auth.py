import typing
from django.contrib.auth.backends import ModelBackend

from django.contrib.auth import get_user_model


# class CustomBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         User = get_user_model()
#         try:
#             user = User.objects.get(email=username)
#         except User.DoesNotExist:
#             return None
#
#         return user if user.check_password(password) else None

    # def get_user(self, user_id) -> typing.Optional[User]:
    #     try:
    #         return User.objects.get(id=user_id)
    #     except User.DoesNotExist:
    #         return None
