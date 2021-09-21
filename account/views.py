import json
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from shopify_first_try import settings
from account.forms import RegisterForm
from .serializers import TokenSerializer, UserSerializerRegister, UserSerializerShow
from .users import *


class AuthenticationAPI(viewsets.ViewSet, generics.GenericAPIView):
    serializer_class = UserSerializerRegister
    queryset = get_user_model()

    def create(self, request):
        print(request.data)
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
        print(email)
        if email is not None:
            if BaseUserModel().getUserByEmail(email):
                return Response({'exists': True})
        return Response({'exists': False})
# class AjaxMixin(FormView):
#     def get_form_kwargs(self):
#         kwargs = {
#             'initial': self.get_initial(),
#             'prefix': self.get_prefix(),
#         }
#
#         if self.request.method in ('POST', 'PUT'):
#             kwargs.update({
#                 'data': json.loads(self.request.body.decode("utf-8")),
#                 'files': self.request.FILES,
#             })
#
#         return kwargs
#
#
# class AuthenticationView(AjaxMixin, FormView):
#     form_class = RegisterForm
#     template_name = 'index.html'
#     def form_valid(self, form):
#         try:
#             self.authenticateUser(form)
#             return JsonResponse({'server_response': 'succeed'})
#         except:
#             return JsonResponse({'server_response': 'fail'})
#
#     def authenticateUser(self, form):
#         user = UserDataStructure(**form.data)
#         if form.data.get('action') == 'login':
#             self.logUserIn(user)
#         else:
#             login(self.request, self.registerUser(user))
#
#     def logUserIn(self, user):
#         BaseUserModel(self.request).logUserIn(user)
#
#     def registerUser(self, user):
#         return BaseUserModel(self.request).register(user)
#
#     def form_invalid(self, form):
#         return JsonResponse({'server_response': 'fail'})
#
#
# def CheckUsernameExistence(request):
#     data = request.GET
#     return JsonResponse({'server_response': 'exist'}) if User.objects.filter(
#         username=data['email']).count() != 0 else JsonResponse({'server_response': 'free'})
#
#
# class GeneralInfo(TemplateView):
#     def get(self, request, *args, **kwargs):
#         return JsonResponse(self.loadData())
#
#     @staticmethod
#     def loadData():
#         data = {"authentication": settings.BASE_URL + reverse_lazy('account:authentication'),
#                 'checkuserexistance': settings.BASE_URL + reverse_lazy('account:checkuserexistance')
#                 }
#         return data
