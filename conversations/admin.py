from django.contrib import admin
from .models import Chat,chat_members

admin.site.register(Chat)
admin.site.register(chat_members)

