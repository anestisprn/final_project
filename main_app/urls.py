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

    path("dashboardGuide/experienceUpdate/<int:id>", experienceUpdate, name="experienceUpdate"),
    path("dashboardGuide/experienceDelete/<int:id>", experienceDelete, name="experienceDelete"),


    path("dashboardUser/", dashboardUser, name="dashboardUser"),
    path("dashboardUser/wishList/", wishList, name="wishList"),
    path("dashboardUser/wishList/<int:idUser>/<int:idTour>", wishListAdd, name="wishListAdd"),
    path("dashboardUser/wishList/<int:id>", wishListDrop, name="wishListDrop"),
    path('dashboardUser/editUser/', editUser, name='editUser'),

    path('dashboardUser/orderHistory/', OrderHistoryListView.as_view(), name='orderHistory'),
    path('dashboardGuide/create/', ExperienceCreateView.as_view(), name='create'),
    path('experienceList/', ExperienceListView.as_view(), name='experienceList'),
    path("experienceDetails/<int:id>", ExperienceDetails.as_view(), name="experienceDetails"),
    
    path('success/', PaymentSuccessView.as_view(), name="success"),
    path('failed/', PaymentFailedView.as_view(), name='failed'),

    path('api/checkout-session/<id>/', create_checkout_session, name='api_checkout_session'),
]
