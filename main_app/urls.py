from django.urls import path
from .views import *
urlpatterns = [
    path('', homepage, name='homepage'),
    path("login/", login_user, name="login_user"),
    path("logout/", logout_user, name="logout_user"),
    path('signup_user/', signup_user, name='signup_user'),
    path('signup_guide/', signup_guide, name='signup_guide'),
    path('dashboard/', dashboard, name='dashboard'),

]
