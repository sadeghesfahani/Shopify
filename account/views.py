import json
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from shopify_first_try import settings
from account.forms import RegisterForm
from .users import *


class AjaxMixin(FormView):
    def get_form_kwargs(self):
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': json.loads(self.request.body.decode("utf-8")),
                'files': self.request.FILES,
            })

        return kwargs


class AuthenticationView(AjaxMixin, FormView):
    form_class = RegisterForm

    def form_valid(self, form):
        try:
            self.authenticateUser(form)
            return JsonResponse({'server_response': 'succeed'})
        except:
            return JsonResponse({'server_response': 'fail'})

    def authenticateUser(self, form):
        user = UserDataStructure(**form.data)
        if form.data.get('action') == 'login':
            self.logUserIn(user)
        else:
            login(self.request, self.registerUser(user))

    def logUserIn(self, user):
        BaseUserModel(self.request).logUserIn(user)

    def registerUser(self, user):
        return BaseUserModel(self.request).register(user)

    def form_invalid(self, form):
        return JsonResponse({'server_response': 'fail'})


def CheckUsernameExistence(request):
    data = request.GET
    return JsonResponse({'server_response': 'exist'}) if User.objects.filter(
        username=data['email']).count() != 0 else JsonResponse({'server_response': 'free'})


class GeneralInfo(TemplateView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(self.loadData())

    @staticmethod
    def loadData():
        data = {"authentication": settings.BASE_URL + reverse_lazy('account:authentication'),
                'checkuserexistance': settings.BASE_URL + reverse_lazy('account:checkuserexistance')
                }
        return data
