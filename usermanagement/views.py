from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, ChangePasswordSerializer
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .token import get_user_token
from .models import *
from rest_framework.generics import UpdateAPIView
import random
import smtplib
import tempfile
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

class RegisterUser(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        data = request.data
        serializer = UserSerializer(data=data)
        if not serializer.is_valid():
            errors = serializer.errors
            print(errors)
            return Response({'save': False, 'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            email = data['email']
            user = User.objects.filter(email=email)
            if user:
                message = {'status': False, 'message': 'email already exists'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            message = {'save': True}
            return Response(message)

        message = {'save': False, 'errors': serializer.errors}
        return Response(message)
# {
# "first_name":"Ditso",
# "last_name":"Ditso",
# "email":"ditsohealth@dit.co.tz",
# "password":"ditsohealth123",
# "username":"DitsoHealth",
# "phone_number":"078676726",
# "role":4,
# }


class CreateUserTemporary(APIView):
    @staticmethod
    def post(request):
        try:
            data = request.data

            full_name = data.get('full_name')
            registration_no = data.get('registration_no')
            email = data.get('email')
            password = data.get('password')
            username = data.get('username')
            role = data.get('role', UserTemporary.NORMAL_USER)
            course = data.get('course')
            class_name = data.get('class_name')
            campus_id = data.get('campus')

            user = UserTemporary.objects.create(
                full_name=full_name,
                registration_no=registration_no,
                email=email,
                password=password,
                username=username,
                role=role,
                course=course,
                class_name=class_name,
                campus=campus_id
            )

            return Response({'message': 'User created waiting for fingerprint for registration completion', 'user_id': user.id}, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class RegisterUserWithFingerPrint(APIView):
    @staticmethod
    def post(request):
        try:
            data = request.data

            user_dt = UserTemporary.objects.all()
            print(user_dt)
            user_temp = user_dt[0]
            print(user_temp)

            user_data = {
                'full_name': user_temp.full_name,
                'registration_no': user_temp.registration_no,
                'email': user_temp.email,
                'password': user_temp.password,
                'username': user_temp.username,
                'role': user_temp.role,
                'course': user_temp.course,
                'class_name': user_temp.class_name,
                'fingerprint_images': data.get("fingerprint_data"),
                'campus': user_temp.campus
            }

            # Serialize the data
            serializer = UserSerializer(data=user_data)
            if serializer.is_valid():
                # Create the user
                serializer.save()

                # Delete the temporary user data
                user_temp.delete()

                return Response({'message': 'User created successfully', 'user_id': serializer.data['id']},
                                status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserTemporary.DoesNotExist:
            return Response({'error': 'user data not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        email = request.data.get('email')
        password = request.data.get('password')
        print('Data:', email, password)
        user = authenticate(email=email, password=password)

        if user is not None:
            otp = random.randint(1000, 9999)

            if LoginView.send_otp_email(email, otp):
                login(request, user)
                user_id = User.objects.get(email=email)
                new_otp = UserOtps(user=user_id, otp=otp)
                new_otp.save()
                user_info = UserSerializer(instance=user_id, many=False).data
                response = {
                    'user': user_info,
                    'success': True,
                    'otp': otp
                }
                return Response(response)
            else:
                return Response({'message': 'Email sending failed'}, status=500)

        return Response({'msg': 'Invalid username or password'}, status=401)

    @staticmethod
    def send_otp_email(email, otp):
        try:
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            smtp_username = "neychimfocus@gmail.com"
            smtp_password = "qzltsoowsqqmxvwt"
            smtp_sender = "neychimfocus@gmail.com"
            smtp_recipient = email

            message = MIMEMultipart()
            message['From'] = smtp_sender
            message['To'] = smtp_recipient
            message['Subject'] = 'DIT E-VOTING SYSTEM.'

            text = (f"DIT E-VOTING SYSTEM\n\n\n"
                    f"LOGIN AUTHENTICATION ONE TIME PASSWORD\n"
                    f"Your OTP: {otp}\n for {email}"
                    f"Enter this OTP for Authorization."
                    f"This otp will expire in 10 mins")
            message.attach(MIMEText(text))

            print("Connecting to SMTP server...")
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                print("Starting TLS...")
                server.login(smtp_username, smtp_password)
                print("Logged in to SMTP server...")
                server.sendmail(smtp_sender, smtp_recipient, message.as_string())
                print("Email sent to", smtp_recipient)

            return True

        except Exception as e:
            print(f"Error sending email: {e}")
            return False



class VerifyOtps(APIView):
    @staticmethod
    def post(request):
        otpstr = request.data.get("otp")
        user_id_req = request.data.get("user_id")
        print(request.data)
        otp = otpstr
        try:
            user_in_otp = UserOtps.objects.get(user=user_id_req)
            print(user_in_otp,"--------------")
            if otp == user_in_otp.otp:
                user_id = User.objects.get(id=user_id_req)
                user_info = UserSerializer(instance=user_id, many=False).data
                print("==================================================")
                print(user_info)
                response = {
                    'token': get_user_token(user_id),
                    'user': user_info,
                    'success': True,
                }
                return Response(response)
            else:
                response = {
                    'message': "Invalid Otp",
                    'success': False,
                }
                return Response(response)
        except UserOtps.DoesNotExist:
            response = {
                'message': "Invalid User",
                'success': False,
            }
            return Response(response)
        finally:
            # Ensure the OTP record is deleted if it exists
            try:
                user_in_otp = UserOtps.objects.get(user=user_id_req)
                user_in_otp.delete()
            except UserOtps.DoesNotExist:
                pass


# {
#     "email":"neemajames11@yahoo.com",
#     "password":"chimpaye"
# }


class UserInformation(APIView):

    @staticmethod
    def get(request):
        query_type = request.GET.get("querytype")
        if query_type == 'single':
            try:
                user_id = request.GET.get('user_id')
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'message': 'User Does Not Exist'})
            return Response(UserSerializer(instance=user, many=False).data)

        elif query_type == 'all':
            queryset = User.objects.all()
            return Response(UserSerializer(instance=queryset, many=True).data)

        else:
            return Response({'message': 'Wrong Request!'})


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
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
                'status': True,
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserChangeRoles(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        id = request.data['id']
        role = request.data['role']

        try:
            user = User.objects.get(id=id)

            if user:
                user.role = role
                user.save()
            return Response({'save': True, "user": UserSerializer(instance=user, many=False).data})
        except User.DoesNotExist:
            return Response({'save': False, 'message': 'User doest exist'})


class UpdateUserView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        gender = request.data['gender']
        email = request.data['email']
        fname = request.data['fname']
        profile = request.data['profile']
        lname = request.data['lname']
        phone_number = request.data['phone_number']
        if phone_number:
            try:
                query = User.objects.get(email=email)
                query.email = email
                query.first_name = fname
                query.last_name = lname
                query.gender = gender
                query.phone_number = phone_number
                query.profile = profile
                query.save()
                return Response({'save': True, "user": UserSerializer(instance=query, many=False).data})
            except User.DoesNotExist:
                return Response({'message': 'You can not change the email'})

        else:

            return Response({'message': 'Not Authorized to Update This User'})


class LoggedInUser(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        user = request.user

        if user:
            loggedin = User.objects.get(email=user.email)
            return Response(UserSerializer(instance=loggedin, many=False).data)
        else:
            message = {
                "loggedIn": False,
                "msg": "Loggin session expired"
            }
            return Response(message)