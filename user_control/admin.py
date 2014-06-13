from django.contrib import admin
from django.contrib.contenttypes import generic
from user_control.models import UserProfile

admin.site.register(UserProfile)