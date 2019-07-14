from django.db import models

from django.contrib.auth.models import AbstractUser
from hackathons.models import Hackathon, Sponsorship

# Create your models here.


class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    current_hackathon = models.ForeignKey(
        Hackathon, on_delete=models.SET_NULL, null=True, related_name="users"
    )
    sponsorships = models.ManyToManyField(
        Sponsorship, blank=True, related_name="organizer_contacts"
    )

    def __str__(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username