from django.contrib import admin
from .models import Profile, Message_url


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "external_id", "name", "first_name", "l_name", "created_at")


@admin.register(Message_url)
class Message_url(admin.ModelAdmin):
    list_display = ('id', 'profile', 'text', 'created_at')
