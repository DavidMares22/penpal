from django.urls import path
from .views import *

app_name = 'pages'

urlpatterns = [
    path('', index, name="index"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("register/", register, name="register"),
    path("profile/<int:profile_id>", profile, name="profile"),
    path("request/send/<int:to_profile_id>", send_request, name="send_request"),
    path("request/accept/<int:from_profile_id>", accept_friend_request, name="accept_request"),
    path("request/delete/<int:from_profile_id>", delete_friend_request, name="delete_request"),
    path("request/cancel/<int:to_profile_id>", cancel_request, name="cancel_request"),
    path("edit/",edit_profile,name="edit"),
    path("search/",search,name="search"),
    path("unfriend/<int:profile_id>",unfriend,name="unfriend"),
    
    
]