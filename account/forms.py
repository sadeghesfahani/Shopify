from django import forms
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
User = get_user_model()


class RegisterForm(forms.Form):
    fname = forms.CharField(max_length=60, label='نام: ', widget=forms.TextInput(attrs={'class': 'form-control'}))
    lname = forms.CharField(max_length=60, label='نام خانوادگی: ',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='ایمیل: ', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='کلمه عبور: ')
    url = forms.CharField(widget=forms.HiddenInput,initial=reverse_lazy('account:checkusernameexistance'))

    def registerUser(self):
        user = User()

        return self.setUserData(user)

    def setUserData(self, user):
        user.first_name = self.cleaned_data['fname']
        user.last_name = self.cleaned_data['lname']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.user_type = User.CUSTOMER
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user
