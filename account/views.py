import json

from django.contrib.auth import login
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import get_user_model

from account.forms import RegisterForm

User = get_user_model()


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        print(form)
        user = form.registerUser()
        login(self.request, user)
        return JsonResponse({'server_response': 'succeed'})

    def get_form_kwargs(self):
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }

        if self.request.method in ('POST', 'PUT'):
            # print(json.loads(self.request.body.decode("utf-8")))
            kwargs.update({
                'data': json.loads(self.request.body.decode("utf-8")),
                'files': self.request.FILES,
            })
        return kwargs

    # def get_form(self, form_class=None):
    #     """Return an instance of the form to be used in this view."""
    #     if form_class is None:
    #         form_class = self.get_form_class()
    #     return form_class(**self.get_form_kwargs())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        print(form)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


def CheckUsernameExistence(request):
    data = json.loads(request.body.decode("utf-8"))
    return JsonResponse({'server_response': 'exist'}) if User.objects.filter(
        email=data['email']).count() != 0 else JsonResponse({'server_response': 'free'})
