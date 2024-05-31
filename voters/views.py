import subprocess
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import Usersserializer, ChangePasswordSerializer
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .token import get_user_token
from .models import Users
from rest_framework.generics import UpdateAPIView
import time
from django.http import StreamingHttpResponse, HttpResponseServerError, JsonResponse
from rest_framework.decorators import api_view, permission_classes
import datetime


class RegisterUser(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        data = request.data
        print(request.data)
        serializer = Usersserializer(data=data)
        if serializer.is_valid():
            email = data['email']
            user = Users.objects.filter(email=email)
            if user:
                message = {'status': False, 'message': 'Username already exists'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

            message = {'save': True}
            return Response(message)

        message = {'save': False, 'errors': serializer.errors}
        return Response(message)


class LoginView(APIView):

    @staticmethod
    def post(request):
        email = request.data.get('email')
        password = request.data.get('password')
        print('Data: ', email, password)
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            user_id = Users.objects.get(email=email)
            print(user_id)
            user_info = Usersserializer(instance=user_id, many=False).data
            print(user_info)
            print("---------------------------------here")
            response = {
                'token': get_user_token(user_id),
                'user': user_info
            }

            return Response(response)
        else:
            response = {
                'msg': 'Invalid username or password',
            }

            return Response(response)

class ReturnUsersView(APIView):

    def get(self, request):
        userData = []
        obj = Users.objects.all().values()
        for user in obj:
            if user['is_staff'] == False:
                userData.append(user)

        return Response(userData)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = Users
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)