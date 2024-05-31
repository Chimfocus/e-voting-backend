from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import date, datetime


# Create your models here.

class Users(AbstractUser):
  ADMIN = 0
  NORMAL_USER = 1
  role_choices = (
    (ADMIN, 'ADMIN'),
    (NORMAL_USER, 'NORMAL_USER'),
  )

  user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  first_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  email = models.EmailField(unique=True)
  phone_number = models.CharField(max_length=12)
  gender_choice = (
    ('M', 'MALE'),
    ('F', 'FEMALE'),
  )

  gender = models.CharField(choices=gender_choice, max_length=2)
  position = models.CharField(max_length=100)
  date_of_birth = models.DateTimeField(null=True)
  role = models.IntegerField(choices=role_choices, default=NORMAL_USER)

  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = ['phone_number', 'username']

  def __str__(self):
    return self.email