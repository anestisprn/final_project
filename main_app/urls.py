from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path("tourExperience/", tourExperience, name="tourExperience"),
    path("contactUs/", contactUs, name="contactUs"),

    path("login/", loginUser, name="loginUser"),
    path("logout/", logoutUser, name="logoutUser"),
    path("signupUser/", signupUser, name="signupUser"),
    path("signupGuide/", signupGuide, name="signupGuide"),

    path("dashboardGuide/", dashboardGuide, name="dashboardGuide"),
    path("dashboardGuide/createActivity/<int:idUser>", createActivity, name="createActivity"),
    path("dashboardGuide/updateActivity/<int:id>", updateActivity, name="updateActivity"),
    path("dashboardGuide/deleteActivity/<int:id>", deleteActivity, name="deleteActivity"),

    path("dashboardUser/", dashboardUser, name="dashboardUser"),
    # path("dashboardUser/joinActivity/<int:idUser>/<int:idTour>", joinActivity, name="joinActivity"),
    # path("dashboardUser/dropActivity/<int:id>", dropActivity, name="dropActivity"),

    path("experienceDetails/<int:id>", ExperienceDetails.as_view(), name="experienceDetails"),
    path('api/checkout-session/<id>/', create_checkout_session, name='api_checkout_session'),

    path('success/', PaymentSuccessView.as_view(), name="success" ),
]
