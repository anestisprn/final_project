from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import PasswordChangeForm
from .forms import *
from .models import *

# Create your views here.
def homepage(request):
    context = {'allToursList': TourExperience.objects.all()}
    return render(request, 'main_app/homepage.html', context)

def tourExperience(request):
    context = {'allToursList': TourExperience.objects.all()}
    return render(request, 'main_app/tourExperience.html', context)

def contactUs(request):
    context = {}
    return render(request, 'main_app/contactUs.html', context)


def signupUser(request):
    if request.method == "POST":
        # form validation, save new user object, authenticate and login user
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("homepage")
    else:
        form = UserRegistrationForm()
    return render(request, "main_app/signupUser.html", {"form": form})


def signupGuide(request):
    if request.method == 'POST':
        form = GuideRegistrationForm(request.POST)
        if form.is_valid():
            form.save()            
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password)
            login(request,user)
            return redirect('homepage')
    else:
        form = GuideRegistrationForm()
    return render(request, 'main_app/signupGuide.html', {'form':form})


def loginUser(request):
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect("homepage")
            else:
                return redirect('login')
    else:
        form = LoginForm()
    return render (request, "main_app/login.html", {'form':form})


# @ login_required(login_url='login')
# def changePassword(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             form.save()
#             user = authenticate(request, username=request.user.username,
#                                 password=form.cleaned_data.get('new_password2'))

#             login(request, user)
#             message = 'You have successfully changed your password'
#             return redirect('success', message=message)
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'main_app/changePassword.html', {'form': form})


def logoutUser(request):
    logout(request)
    return redirect("homepage")


@ login_required(login_url='login')
def dashboardGuide(request):
    allToursList = TourExperience.objects.all()
    context = {'allToursList': allToursList}
    return render(request,'main_app/dashboardGuide.html', context)


@ login_required(login_url='login')
def createActivity(request, id):
    context = {}
    if request.method == 'POST':
        if request.user.tourguide.isGuideApproved == 'Approved': 
            newExperience = TourExperience()
            newExperience.tourTitle = request.POST['experienceTitle']
            newExperience.tourLocation = request.POST['experienceLocation']
            newExperience.tourDuration = request.POST['experienceDuration']
            newExperience.tourPrice = request.POST['experiencePrice']
            newExperience.tourAvailableDate = request.POST['experienceAvailableDate']
            newExperience.tourMaxNumberOfPeople = request.POST['experienceMaxNumPeople']
            newExperience.tourDescription = request.POST['experienceDescription']
            # newExperience.tourImage = request.POST['experienceImage']
            currentGuide = TourGuide.objects.get(id=id)
            newExperience.tourGuide = currentGuide

            if not newExperience.tourTitle:
                context['emptyExperienceTitle'] = 'Please enter an experience title'
            elif not newExperience.tourLocation:
                context['emptyExperienceLocation'] = 'Please enter an experience location'            
            elif not newExperience.tourDuration:
                context['emptyExperienceDuration'] = 'Please enter an experience duration'     
            elif not newExperience.tourPrice:
                context['emptyExperiencePrice'] = 'Please enter an experience price'     
            elif not newExperience.tourAvailableDate:
                context['emptyExperienceAvailableDate'] = 'Please enter an experience date'                    
            elif not newExperience.tourMaxNumberOfPeople:
                context['emptyExperienceMaxNumPeople'] = 'Please enter a maximum number of people'     
            elif not newExperience.tourDescription:
                context['emptyExperienceDescription'] = 'Please enter an experience description'     
            # elif not newExperience.tourImage:
            #     context['emptyExperienceImage'] = 'Please enter an experience image'  
            # elif newExperience is not None:
            newExperience.save()
            return redirect("homepage")
    return render(request,'main_app/createActivity.html', context)


@ login_required(login_url='login')
def updateActivity(request, id):
    context = {}    
    return render(request, 'main_app/updateActivity.html', context)


@ login_required(login_url='login')
def deleteActivity(request, id):
    context = {}    
    return render(request, 'main_app/deleteActivity.html', context)


@ login_required(login_url='login')
def dashboardUser(request):
    allToursList = TourExperience.objects.all()
    context = {'allToursList': allToursList}
    return render(request, 'main_app/dashboardUser.html', context)


@ login_required(login_url='login')
def joinActivity(request, id):
    context = {}    
    return render(request, 'main_app/joinActivity.html', context)


@ login_required(login_url='login')
def dropActivity(request, id):
    context = {}    
    return render(request, 'main_app/dropActivity.html', context)
