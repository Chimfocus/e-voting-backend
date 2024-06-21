from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class Campus(models.Model):
    id = models.AutoField(primary_key=True)
    campus_name = models.CharField(max_length=255)
    campus_location = models.CharField(max_length=255)

    def __str__(self):
        return self.campus_name


class User(AbstractUser):
    # Define choices for system roles
    ADMIN = 0
    NORMAL_USER = 1

    # Choices for gender
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    SYSTEM_ROLES = (
        (ADMIN, 'ADMIN'),
        (NORMAL_USER, 'NORMAL_USER')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    registration_no = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    role = models.PositiveIntegerField(choices=SYSTEM_ROLES, default=NORMAL_USER)
    course = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='pictures/', null=True, blank=True)
    fingerprint_images = models.TextField(null=True, blank=True)
    campus = models.OneToOneField(Campus,null=True,blank=True, on_delete=models.CASCADE)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', "username"]

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'


class UserOtps(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, models.CASCADE)
    otp = models.IntegerField()


    
