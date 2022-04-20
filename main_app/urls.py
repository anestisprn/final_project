from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path("contactUs/", contactUs, name="contactUs"),

    path("login/", loginUser, name="loginUser"),
    path("logout/", logoutUser, name="logoutUser"),
    path("signupUser/", signupUser, name="signupUser"),
    path("signupGuide/", signupGuide, name="signupGuide"),


    path("dashboardGuide/", dashboardGuide, name="dashboardGuide"),

    path("dashboardUser/", dashboardUser, name="dashboardUser"),
    path("dashboardUser/wishList/", wishList, name="wishList"),
    path("dashboardUser/wishList/<int:idTour>", wishListAdd, name="wishListAdd"),
    path("dashboardUser/wishList/<int:id>", wishListDrop, name="wishListDrop"),
    path('dashboardUser/editUser/', editUser, name='editUser'),

    path('dashboardUser/orderHistory/', OrderHistoryListView.as_view(), name='orderHistory'),
    path('dashboardGuide/experienceCreate/', ExperienceCreateView.as_view(), name='experienceCreate'),
    path("dashboardGuide/experienceUpdate/<int:id>", ExperienceUpdateView.as_view(), name="experienceUpdate"),
    path("dashboardGuide/experienceDelete/<int:id>", ExperienceDeleteView.as_view(), name="experienceDelete"),
    path('experienceList/', ExperienceListView.as_view(), name='experienceList'),
    path("experienceDetails/<int:id>", ExperienceDetails.as_view(), name="experienceDetails"),
    
    path('success/', PaymentSuccessView.as_view(), name="success"),
    path('failed/', PaymentFailedView.as_view(), name='failed'),

    path('api/checkout-session/<id>/', create_checkout_session, name='api_checkout_session'),

    #sorting paths for price
    path('sortByPriceAscending/', sortByPriceAscending, name="sortByPriceAscending"),
    path('sortByPriceDescending/', sortByPriceDescending, name="sortByPriceDescending"),

    #sorting paths for maximum number of people
    path('sortByNumberOfPeopleAscending/', sortByNumberOfPeopleAscending, name="sortByNumberOfPeopleAscending"),
    path('sortByNumberOfPeopleDescending/', sortByNumberOfPeopleDescending, name="sortByNumberOfPeopleDescending"),

    #sorting paths for maximum number of people
    path('sortByDurationAscending/', sortByDurationAscending, name="sortByDurationAscending"),
    path('sortByDurationDescending/', sortByDurationDescending, name="sortByDurationDescending"),

    #sorting paths for maximum number of people
    path('sortByDateAscending/', sortByDateAscending, name="sortByDateAscending"),
    path('sortByDateDescending/', sortByDateDescending, name="sortByDateDescending"),
]
