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
            registration_no = data['registration_no']
            user = Users.objects.filter(email=email)
            if user:
                message = {'status': False, 'message': 'User already exists'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

            message = {'save': True}
            return Response(message)

        message = {'save': False, 'errors': serializer.errors}
        return Response(message)


class LoginView(APIView):

    @staticmethod
    def post(request):
        registration_no = request.data.get('registration_no')
        secret_code = request.data.get('secret_code')
        print('Data: ', registration_no, secret_code)
        user = authenticate(registration_no=registration_no, secret_code=secret_code)

        if user is not None:
            login(request, user)
            user_id = Users.objects.get(registration_no=registration_no)
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
                'msg': 'Invalid entry',
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