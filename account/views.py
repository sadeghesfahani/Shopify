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
        user = form.registerUser()
        login(self.request, user)
        super(RegisterView, self).form_valid(form)

    def form_invalid(self, form):
        super(RegisterView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['req'] = 'register'
        return context


def CheckUsernameExistence(request):
    data = json.loads(request.body.decode("utf-8"))
    return JsonResponse({'server_response': 'exist'}) if User.objects.filter(
        email=data['username']).count() != 0 else JsonResponse({'server_response': 'free'})
