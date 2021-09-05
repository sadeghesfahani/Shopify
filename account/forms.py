from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class RegisterForm(forms.Form):
    fname = forms.CharField(max_length=60)
    lname = forms.CharField(max_length=60)
    email = forms.EmailField()
    password = forms.CharField()

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

    def getUser(self):
        return authenticate(username=self.cleaned_data['email'], password=self.cleaned_data['password'])


