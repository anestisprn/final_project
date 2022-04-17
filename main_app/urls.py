from django.urls import path
from .views import *
urlpatterns = [
    path('', homepage, name='homepage'),
    # path('login/', login, name='login'),
    path('signup_guide/', signup_guide, name='signup_guide'),
    path("login/", login_user, name="login_user"),
    path("logout/", logout_user, name="logout_user"),
    path('signup_user/', signup_user, name='signup_user'),
    path('dashboard_guide/', dashboard_guide, name='dashboard_guide'),
    path('dashboard_user/', dashboard_user, name='dashboard_user'),
]
