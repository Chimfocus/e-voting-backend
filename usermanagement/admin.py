from django.contrib import admin
from .models import User, UserOtps

# Register your models here.
admin.site.register(User)
admin.site.register(UserOtps)