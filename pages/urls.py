from django.urls import path
from .views import *

app_name = 'pages'

urlpatterns = [
    path('', index, name="index"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("register/", register, name="register"),
    path("profile/<int:profile_id>", profile, name="profile"),
    path("request/send/<int:to_user_id>", send_request, name="send_request"),
    path("request/accept/<int:from_user_id>", accept_friend_request, name="accept_request"),
    path("request/delete/<int:from_user_id>", delete_friend_request, name="delete_request"),
    path("request/cancel/<int:to_user_id>", cancel_request, name="cancel_request"),
    path("edit/",edit_profile,name="edit"),
    path("search/",search,name="search"),
    
    
]