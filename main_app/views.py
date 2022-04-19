from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from matplotlib.style import context
# from django.contrib.auth.forms import PasswordChangeForm
from .forms import *
from .models import *
from django.views.generic import ListView, CreateView, DetailView, TemplateView
import stripe
from django.conf import settings
from django.http.response import HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.urls import reverse, reverse_lazy
from django.contrib import messages

# Create your views here.


def homepage(request):
    context = {'allToursList': TourExperience.objects.all()}
    return render(request, 'main_app/homepage.html', context)

# def experienceList(request):
#     context = {'allToursList': experienceList.objects.all()}
#     return render(request, 'main_app/experienceList.html', context)


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
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('homepage')
    else:
        form = GuideRegistrationForm()
    return render(request, 'main_app/signupGuide.html', {'form': form})


def loginUser(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("homepage")
            else:
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, "main_app/login.html", {'form': form})


@login_required
def editUser(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='dashboardUser')
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'main_app/editUser.html', {'user_form': user_form})


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
    return render(request, 'main_app/dashboardGuide.html', context)


@ login_required(login_url='login')
def createActivity(request, idUser):
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
            currentGuide = TourGuide.objects.get(id=idUser)
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
            return redirect("dashboardGuide")
    return render(request, 'main_app/createActivity.html', context)


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
    allWishList = WishList.objects.all()
    context = {
        'allToursList': allToursList,
        'allWishList': allWishList
    }
    return render(request, 'main_app/dashboardUser.html', context)

@ login_required(login_url='login')
def wishList(request):
    allToursList = TourExperience.objects.all()
    allWishList = WishList.objects.filter(endUser=request.user)
    context = {
        'allToursList': allToursList,
        'allWishList': allWishList
    }
    return render(request, 'main_app/wishList.html', context)


@ login_required(login_url='login')
def wishListAdd(request, idUser, idTour):
    context = {}
    if request.method == 'POST':
        currentUser = EndUser.objects.get(id=idUser)
        currentExperience = TourExperience.objects.get(id=idTour)
        addWishList = WishList(endUser=currentUser,
                           tourExperience=currentExperience)
        addWishList.save()
        context = {
            'addWishList': addWishList
        }
        return redirect("dashboardUser")
    return render(request, 'main_app/homepage.html', context)

###############################################################################

# @ login_required(login_url='login')
# def dropActivity(request, id):
#     context = {}
#     return render(request, 'main_app/dashboardUser.html', context)

###############################################################################

class ExperienceListView(ListView):
    model = TourExperience
    template_name = "main_app/experienceList.html"
    context_object_name = "allToursList"

# class ExperienceCreateView(CreateView):
#     model = TourExperience
#     fields = '__all__'
#     template_name = "main_app/experienceCreate.html"
#     success_url = reverse_lazy("homepage")


class ExperienceDetails(DetailView):
    model = TourExperience
    template_name = "main_app/experienceDetail.html"
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(ExperienceDetails, self).get_context_data(**kwargs)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


class PaymentSuccessView(TemplateView):
    template_name = "main_app/paymentSuccess.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        order = get_object_or_404(
            OrderDetail, stripe_payment_intent=session.payment_intent)
        order.has_paid = True
        order.save()
        return render(request, self.template_name)


class PaymentFailedView(TemplateView):
    template_name = "main_app/paymentFailed.html"


class OrderHistoryListView(ListView):
    model = OrderDetail
    template_name = "main_app/orderHistory.html"


@csrf_exempt
def create_checkout_session(request, id):

    request_data = json.loads(request.body)
    tourExperience = get_object_or_404(TourExperience, pk=id)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        # Customer Email is optional,
        # It is not safe to accept email directly from the client side
        customer_email=request_data['email'],
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': tourExperience.tourTitle,
                    },
                    'unit_amount': int(tourExperience.tourPrice*100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('success')
        ) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse('failed')),
    )

    order = OrderDetail()
    order.customer_email = request_data['email']
    order.tourExperience = tourExperience
    order.stripe_payment_intent = checkout_session['payment_intent']
    order.amount = int(tourExperience.tourPrice*100)
    order.save()

    # return JsonResponse({'data': checkout_session})
    return JsonResponse({'sessionId': checkout_session.id})
