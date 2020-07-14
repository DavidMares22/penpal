from django.urls import path
from .views import *

app_name = 'conversations'

urlpatterns = [
    path('inbox/<int:profile_friend>', inbox, name="inbox_new_chat"),
    path('inbox/', inbox, name="inbox"),
    path('chatbox/<int:chat_id>', chatbox, name="chatbox"),


]