from django.contrib import admin
from .models import User, UserOtps, RegisteredStudents

# Register your models here.
admin.site.register(User)
admin.site.register(UserOtps)
admin.site.register(RegisteredStudents)