from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import CustomUserManager

class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)

    loaned = models.IntegerField(default=0)
    banned = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
# {
# "email": "first@gmail.com",
# "firstname": "First",
# "lastname": "User",
# "password": "truealphas0"
# }


class Student(models.Model):
    user = models.OneToOneField(AppUser, related_name='student', on_delete=models.CASCADE)
    matric_no = models.CharField(max_length=10, unique=True)

class Lecturer(models.Model):
    user = models.OneToOneField(AppUser, related_name='lecturer', on_delete=models.CASCADE)
    lec_id = models.CharField(max_length=10, unique=True)