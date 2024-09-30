from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from management.models import User_details

# Registering the User_details model
admin.site.register(User_details)
