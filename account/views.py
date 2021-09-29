from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .serializers import TokenSerializer, UserSerializerRegister, UserSerializerShow, AddressSerializer
from .users import *
from .models import Address as AddressModel
from .address import Address


class AuthenticationAPI(viewsets.ViewSet, generics.GenericAPIView):
    serializer_class = UserSerializerRegister
    queryset = get_user_model()

    @staticmethod
    def create(request):
        structured_user_data = UserDataStructure(**request.data)
        user = BaseUserModel(request).register(structured_user_data)
        BaseUserModel(request).logUserInByInstance(user)
        token_key = BaseUserModel(request).getToken(user)
        token = {'token': token_key}
        return Response(TokenSerializer(token, many=False).data)

    @staticmethod
    def retrieve(request, pk=None):
        user = BaseUserModel(request).getUserByToken(pk)
        if request.user == user:
            return Response(UserSerializerShow(user, many=False).data)
        else:
            raise PermissionDenied('You are not allowed to see others profile information')

    @action(detail=False)
    def is_user_exist(self, request):
        email = request.GET.get('email')
        if email is not None:
            if BaseUserModel().getUserByEmail(email):
                return Response({'exists': True})
        return Response({'exists': False})

    @action(detail=False, methods=['POST'])
    def login(self, request):
        user_data = UserDataStructure(**request.data)
        user = BaseUserModel().getUser(user_data)
        if user.is_admin:
            user_permission = 'admin'
        elif user.is_department_admin:
            user_permission = 'store_admin'
        else:
            user_permission = 'customer'
        if user is not None:
            token = BaseUserModel().getToken(user)
            return Response({"status": True, "token": token, "user_permission": user_permission})
        else:
            return Response({"Status": False})


class AddressAPI(viewsets.ViewSet, generics.GenericAPIView):
    serializer_class = AddressSerializer
    queryset = AddressModel()

    def list(self, request):
        print("here")
        address_object = Address()
        user_addresses = address_object.selectByUser(request.user)
        return Response(self.serializer_class(user_addresses, many=True).data)

    def get_permissions(self):
        self.permission_classes = [permissions.IsAuthenticated]
        return super(AddressAPI, self).get_permissions()
