from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email=models.EmailField(unique=True)
    phone_number=models.CharField(unique=True, max_length=20)