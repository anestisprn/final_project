from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import *

# Create your views here.
def homepage(request):
    context = {'allToursList': TourExperience.objects.all()}
    return render(request, 'main_app/homepage.html', context)


def signup_user(request):
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
    return render(request, "main_app/signup_user.html", {"form": form})


def signup_guide(request):
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
    return render(request, 'main_app/signup_guide.html', {'form':form})


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username , password=password)
            login(request, user)
            return redirect("homepage")
    else:
        form = LoginForm()
    return render (request, "main_app/login.html", {'form':form})


# def login_user(request):
#     myErrors = {}
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(request, username=username , password=password)
#         if user is not None:
#             login(request, user)
#             return redirect("homepage")
#         else:
#             if not username:
#                 myErrors["empty_username"] = "please enter username"
#             elif not password:
#                 myErrors["empty_password"] = "please enter password"
#             elif user is None:
#                 myErrors["invalid"] = "Username and password do not match"
#     return render (request, "main_app/login.html", myErrors)


def logout_user(request):
    logout(request)
    return redirect("homepage")


def dashboard_guide(request):
    allToursList = TourExperience.objects.all()
    context = {'allToursList': allToursList}
    return render(request, 'main_app/dashboard_guide.html', context)


def dashboard_user(request):
    allToursList = TourExperience.objects.all()
    context = {'allToursList': allToursList}
    return render(request, 'main_app/dashboard_user.html', context)

def guide_creates_activity(request, id):
    errors = {}
    if request.method == 'POST':
        newExperienceTitle = request.POST['experience_title']
        newExperienceLocation = request.POST['experience_location']
        newExperienceDuration = request.POST['experience_duration']
        newExperiencePrice = request.POST['experience_price']
        newTourAvailableDate = request.POST['experience_available_date']
        newTourMaxNumberOfPeople = request.POST['experience_tour_max_num_people']
        newTourDescription = request.POST['experience_description']
        currentGuide = User.objects.get(pk = request.user.id)
        newTourImage = request.POST['experience_tour_image']

        if request.user.tourguide.isGuideApproved == 'Approved': 
            createExperience = TourExperience()
            createExperience.tourTitle = newExperienceTitle
            createExperience.tourLocation = newExperienceLocation
            createExperience.tourDuration = newExperienceDuration
            createExperience.tourPrice = newExperiencePrice
            createExperience.tourAvailableDate = newTourAvailableDate
            createExperience.tourMaxNumberOfPeople = newTourMaxNumberOfPeople
            createExperience.tourDescription = newTourDescription
            # createExperience.tourGuide = newTourGuide #to get guide based on id
            createExperience.tourGuide = currentGuide
            createExperience.tourImage = newTourImage
            createExperience.save()

            if not newExperienceTitle:
                errors['empty_experience_title'] = 'Please enter an experience title'
            if not newExperienceLocation:
                errors['empty_experience_location'] = 'Please enter an experience location'            
            if not newExperienceDuration:
                errors['empty_experience_duration'] = 'Please enter an experience duration'     
            if not newExperiencePrice:
                errors['empty_experience_price'] = 'Please enter an experience price'     
            if not newTourAvailableDate:
                errors['empty_experience_available_date'] = 'Please enter an experience date'                    
            if not newTourMaxNumberOfPeople:
                errors['empty_experience_max_num_people'] = 'Please enter a maximum number of people'     
            if not newTourDescription:
                errors['empty_experience_description'] = 'Please enter an experience description'     
            if not newTourImage:
                errors['empty_experience_image'] = 'Please enter an experience image'    

    return render(request,'main_app/dashboard.html', errors)


def addTour(request, id):
    tourToAdd = TourExperience.objects.get(id=id)
    userToGet = EndUser.objects.get(user=request.user)
    tourToAdd.tourexperiences.add(userToGet)
    return redirect("homepage")


def tourExperience(request):
    userTourList = TourExperience.objects.get(user=request.user)


# def approveGuide(request):
#     if TourGuide.isGuideApproved == True:
#         show him the content and allow him to create activities.

