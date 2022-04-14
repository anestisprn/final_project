from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import *


from .models import *

# Create your views here.


def homepage(request):
    context = {'allToursList': TourExperience.objects.all()}
    return render(request, 'main_app/homepage.html', context)


def signup_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password)
            return redirect('homepage')
            # login(request, user)
    else:
        form = RegistrationForm()
    
    return render(request,'main_app/signup_user.html', {'form':form})

