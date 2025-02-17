from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SpotifyUser

admin.site.register(SpotifyUser, UserAdmin)