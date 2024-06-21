from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/', include('voters.urls')),
    path('api/auth/', include('usermanagement.urls')),
    path('admin/', admin.site.urls),
]