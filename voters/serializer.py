from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth.forms import PasswordChangeForm
from .models import Users


# class Usersserializer(serializers.ModelSerializer):
#     class Meta:
#         model = Users
#         fields = [
#             'user_id',
#             'first_name',
#             'last_name',
#             'email',
#             'password',
#             'username',
#             'phone_number',
#             'gender',
#             'position',
#             'date_of_birth',
#             'role'
#         ]
#
#         extra_kwargs = {"password": {"write_only: True"}}
#
#         def create(self, validated_data):
#             user = Users.objects.create_user(**validated_data)
#             return user

class Usersserializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'email',

            'username',
            'phone_number',
            'gender',
            'position',
            'date_of_birth',
            'role'
        ]

        extra_kwargs = {
            "password": {"write_only": True}  # Fixed the key-value pair here
        }

    def create(self, validated_data):
        user = Users.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = Users

    new_password = serializers.CharField(required=True)


#class FaceRecordPostSerializer(serializers.ModelSerializer):
    #class Meta:
       # show hierarchical level of data return from request


