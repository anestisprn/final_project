from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm



# class LoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         widgets = {
#             'password': forms.PasswordInput(),
#         }


# class RegistrationForm(ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = EndUser
        fields = ('username', 'first_name', 'last_name', 'userDescription')

class GuideRegistrationForm(UserCreationForm):
    class Meta:
        model = TourGuide
        fields = ('username', 'first_name', 'last_name', 'guideDescription')
        # widgets = {
        #     'guidePassword': forms.PasswordInput(),
        # }
