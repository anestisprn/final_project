from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    path("login/", loginUser, name="loginUser"),
    path("logout/", logoutUser, name="logoutUser"),
    path('signupUser/', signupUser, name='signupUser'),
    path('signupGuide/', signupGuide, name='signupGuide'),
    path('dashboardGuide/', dashboardGuide, name='dashboardGuide'),
    path('dashboardUser/', dashboardUser, name='dashboardUser'),
    path("dashboardGuide/createActivity/<int:id>", createActivity, name="createActivity"),
    path("dashboardUser/joinActivity/<int:id>", joinActivity, name="joinActivity"),
]


