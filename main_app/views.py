from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from .forms import *
from .models import *
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import UpdateView, DeleteView, ListView, CreateView, DetailView, TemplateView
import stripe
from django.conf import settings
from django.http.response import HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.urls import reverse, reverse_lazy
from django.contrib import messages

# Create your views here.

def homepage(request):
    context = {
        'allToursList': TourExperience.objects.all(), 
        'num_of_tours': len(TourExperience.objects.all()), 
        'num_of_guides': len(TourGuide.objects.all()),
        'num_of_purshases': len(OrderDetail.objects.filter(has_paid=True))
        }
    return render(request, 'main_app/homepage.html', context)


class ExperienceListView(ListView):
    model = TourExperience
    template_name = "main_app/experienceList.html"
    context_object_name = "allToursList"
    

def contactUs(request):
    context = {}
    return render(request, 'main_app/contactUs.html', context)


def aboutUs(request):
    context = {}
    return render(request, 'main_app/aboutUs.html', context)


############################ REGISTRATION VIEWS ###################################

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
                messages.warning(request, 'Oops!.. Wrong input try again')
                # return render(request, "main_app/login.html", {'error': 'mitsotaki gamiesai'})
                return redirect('loginUser')
    else:
        form = LoginForm()
    return render(request, "main_app/login.html", {'form': form})


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


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('homepage')


def logoutUser(request):
    logout(request)
    return redirect("homepage")


############################ DASHBOARD USER VIEWS ###################################

def dashboardUser(request):
    labels = []
    data = []
    context = {
        'labels': labels,
        'data': data,
        'num_of_tours': len(WishList.objects.filter(endUser=request.user)), 
        'num_of_bookings': len(OrderDetail.objects.filter(customer_email=request.user.email).filter(has_paid=True)),
        'num_of_outcome': sum(OrderDetail.objects.filter(customer_email=request.user.email).filter(has_paid=True).filter(amount=True))
        }
    queryset = WishList.objects.filter(endUser=request.user).order_by('-tourExperience')[:5]
    for wish in queryset:
        labels.append(wish.tourExperience.tourTitle)
        data.append(wish.tourExperience.tourRating)
    return render(request, 'main_app/dashboardUser.html', context)


def wishList(request):
    allWishList = WishList.objects.filter(endUser=request.user)
    context = {
        'allWishList': allWishList
    }
    return render(request, 'main_app/wishList.html', context)


def wishListAdd(request, id):
    context = {}
    if request.method == 'GET':
        currentUser = EndUser.objects.get(id=request.user.id)
        currentExperience = TourExperience.objects.get(id=id)
        addWishList = WishList(endUser=currentUser,
                            tourExperience=currentExperience)
        addWishList.save()
        context = {
            'addWishList': addWishList
        }
        return redirect("homepage")
    return render(request, 'main_app/wishList.html', context)


class WishListDeleteView(DeleteView):
    model = WishList
    success_url = reverse_lazy("wishList")


############################ DASHBOARD GUIDE VIEWS ###################################

def dashboardGuide(request):
    labels = []
    data = []
    context = {
        'labels': labels,
        'data': data,
        'num_of_tours': len(TourExperience.objects.filter(tourGuide = request.user)), 
        'num_of_bookings': len(TourExperience.objects.filter(tourGuide = request.user).filter()),
        'num_of_income': sum(OrderDetail.objects.filter(customer_email=request.user.email).filter(has_paid=True).filter(amount=True))
        }
    queryset = TourExperience.objects.filter(tourGuide=request.user).order_by('-tourPrice')[:5]
    for tour in queryset:
        labels.append(tour.tourTitle)
        data.append(tour.tourPrice)
    return render(request, 'main_app/dashboardGuide.html', context) 


def experienceManage(request):
    guideToursList = TourExperience.objects.filter(tourGuide=request.user)
    context = {
            'guideToursList': guideToursList,
            }
    return render(request, 'main_app/experienceManage.html', context) 


class ExperienceCreateView(CreateView):
    model = TourExperience
    fields = ('tourTitle', 'tourCity', 'tourCategory', 'tourDuration', 'tourPrice', 'tourAvailableDate', 'tourMaxNumberOfPeople', 'tourDescription', 'tourImage')
    template_name = "main_app/experienceCreate.html"
    success_url = reverse_lazy("dashboardGuide")
    
    def get_form(self):
        from django.forms.widgets import SelectDateWidget
        form = super(ExperienceCreateView, self).get_form()
        form.fields['tourAvailableDate'].widget = SelectDateWidget()
        return form

    def form_valid(self, form):
        form.instance.tourGuide = TourGuide.objects.get(id=self.request.user.id)
        return super(ExperienceCreateView, self).form_valid(form)


class ExperienceUpdateView(UpdateView):
    model = TourExperience
    fields = ('tourTitle', 'tourCity', 'tourCategory', 'tourDuration', 'tourPrice', 'tourAvailableDate', 'tourMaxNumberOfPeople', 'tourDescription', 'tourImage')
    success_url = reverse_lazy("dashboardGuide")


class ExperienceDeleteView(DeleteView):
    model = TourExperience
    success_url = reverse_lazy("dashboardGuide")


############################ PAYMENT VIEWS ###################################

class ExperienceDetails(DetailView):
    model = TourExperience
    template_name = "main_app/experienceDetail.html"
    pk_url_kwarg = 'id'

    def get(self, *args, **kwargs):
        response = super(ExperienceDetails, self).get(*args, **kwargs)
        response ['Content-Security-Policy'] = "frame-ancestors 'self' https://www.openstreetmap.org"
        return response

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


############################ SORTING VIEWS ####################################

def sortByPriceAscending(request):
    allToursList = TourExperience.objects.order_by('tourPrice')
    context = {'allToursList': allToursList}
    return render(request, 'main_app/sortBy.html', context)

def sortByPriceDescending(request):
    allToursList = TourExperience.objects.order_by('-tourPrice')
    context = {'allToursList': allToursList}
    return render(request, 'main_app/sortBy.html', context)


def sortByNumberOfPeopleAscending(request):
    allToursList = TourExperience.objects.order_by('tourMaxNumberOfPeople')
    context = {'allToursList': allToursList}
    return render(request, 'main_app/sortBy.html', context)


def sortByNumberOfPeopleDescending(request):
    allToursList = TourExperience.objects.order_by('-tourMaxNumberOfPeople')
    context = {'allToursList': allToursList}
    return render(request, 'main_app/sortBy.html', context)


def sortByDurationAscending(request):
    allToursList = TourExperience.objects.order_by('tourDuration')
    context = {'allToursList': allToursList}
    return render(request, 'main_app/sortBy.html', context)

def sortByDurationDescending(request):
    allToursList = TourExperience.objects.order_by('-tourDuration')
    context = {'allToursList': allToursList}
    return render(request, 'main_app/sortBy.html', context)

def sortByDateAscending(request):
    allToursList = TourExperience.objects.order_by('tourAvailableDate')
    context = {'allToursList': allToursList}
    return render(request, 'main_app/sortBy.html', context)

def sortByDateDescending(request):
    allToursList = TourExperience.objects.order_by('-tourAvailableDate')
    context = {'allToursList': allToursList}
    return render(request, 'main_app/sortBy.html', context)


# def sortByCategoryDrinking(request):
#     all_tours_list = TourExperience.objects.filter(tourCategory = 'drinking')

#########################################################################



# class SortByView(ListView):
#     all_tours_list = TourExperience.objects.all()
#     sortByPriceAscending = all_tours_list.order_by('-tourPrice')
#     sortByPriceDescending = all_tours_list.order_by('tourPrice')
#     def sortBy():
#         if sortByPriceAscending:
#             context = {'sorted_tour_list': sortByPriceAscending}
#         elif sortByPriceDescending:
#             context = {'sorted_tour_list': sortByPriceDescending}

#         return render(request,'main_app/sortBy.html', context)

###############################################################################