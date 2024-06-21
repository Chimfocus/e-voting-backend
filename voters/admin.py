from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Election)
admin.site.register(Vote)
admin.site.register(Campus)
admin.site.register(Message)
admin.site.register(Candidate)
