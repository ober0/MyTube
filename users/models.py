from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    gender = models.CharField(null=True, blank=True, max_length=10)
    birth_date = models.DateField(null=True, blank=True)
