from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from datetime import date, timezone
import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=50, null=True)
    age = models.IntegerField(null=True, blank=True)
    additional_info = models.CharField(max_length=100, null=True)
    is_admin = models.BooleanField(default=False)
    registration_date = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return f"{self.user.username}"
