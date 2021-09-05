import json
from django.contrib.auth import login
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import get_user_model
from django.views.generic.base import TemplateView
from shopify_first_try import settings
from account.forms import RegisterForm

User = get_user_model()


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
        user = form.registerUser()
        login(self.request, user)
        return JsonResponse({'server_response': 'succeed'})

    def form_invalid(self, form):
        user = form.getUser()
        if user is not None:
            login(self.request, user)
            return JsonResponse({'server_response': 'succeed'})
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
        data = {"register": settings.BASE_URL + reverse_lazy('account:authentication'),
                'checkuserexistance': settings.BASE_URL + reverse_lazy('account:checkuserexistance')
                }
        return data
