from django.urls import path
from . import views

urlpatterns = [
    path('voters/register', views.RegisterUser.as_view(), name='RegisterUser'),
    path('voters/login', views.LoginView.as_view(), name='Login'),
    path('voters/ChangePassword', views.ChangePasswordView.as_view(), name='ChangePassword'),
    path('voters/Users', views.ReturnUsersView.as_view(), name="ReturnUsersView"),
]
