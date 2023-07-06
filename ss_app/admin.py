from django.contrib import admin
from .models import User, chat_history,Chat

# Register your models here.

admin.site.register(User)
admin.site.register(chat_history)
admin.site.register(Chat)