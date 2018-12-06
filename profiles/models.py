from django.db import models

from django.contrib.auth.models import AbstractUser
from hackathons.models import Hackathon

# Create your models here.


class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    current_hackathon = models.ForeignKey(
        Hackathon, on_delete=models.SET_NULL, null=True, related_name="users"
    )

