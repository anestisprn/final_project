from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from .forms import * 


from .models import *

# Create your views here.


def homepage(request):
    context = {'allToursList': TourExperience.objects.all()}
    return render(request, 'main_app/homepage.html', context)


def signup_user(request):
    if request.method == "POST":
        # form validation, save new user object, authenticate and login user
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            guideList = request.POST.getlist("make_guide")
            if guideList:
                guide = TourGuide(user=request.user, is_guide=True)
                guide.save()
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, "main_app/signup_user.html", {"form": form})


def signup_guide(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()            
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password)
            login(request,user)
            return redirect('homepage')
    else:
        form = UserCreationForm()

    return render(request, 'main_app/signup_guide.html', {'form':form})


def login_user(request):
    myErrors = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username , password=password)
        if user is not None:
            login(request, user)
            return redirect("homepage")
        else:
            if not username:
                myErrors["empty_username"] = "please enter username"
            elif not password:
                myErrors["empty_password"] = "please enter password"
            elif user is None:
                myErrors["invalid"] = "Username and password do not match"
    return render (request, "main_app/login.html", myErrors)


def logout_user(request):
    logout(request)
    return redirect("homepage")

def dashboard(request):
    allToursList = TourExperience.objects.all()
    context = {'allToursList': allToursList}
    return render(request, 'main_app/dashboard.html', context)


def guideActivities(request):
    pass

# def approveGuide(request):
#     if TourGuide.isGuideApproved == True:
#         show him the content and allow him to create activities.