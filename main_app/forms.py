from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        widgets = {
            'password': forms.PasswordInput(),
        }


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = EndUser
        fields = ('username', 'first_name', 'last_name', 'email')


class GuideRegistrationForm(UserCreationForm):
    class Meta:
        model = TourGuide
        fields = ('username', 'first_name', 'last_name', 'guideDescription')


# class RegistrationForm(ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ('username', 'password')

# class UpdateUserForm(UserRegistrationForm):
#     pass

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']
