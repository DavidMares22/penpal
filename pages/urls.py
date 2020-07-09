from django.urls import path
from .views import *

app_name = 'pages'

urlpatterns = [
    path('', index, name="index"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("register/", register, name="register"),
    path("profile/", profile, name="profile")
    
]