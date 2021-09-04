from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import FormView

from account.forms import RegisterForm




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
