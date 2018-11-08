from django.db import models
from django.utils import timezone

from profiles.models import User


class Email(models.Model):
    """Object representing the Contact."""

    STATUS_CHOICES = {("sent", "Sent"), ("draft", "Draft"), ("scheduled", "Scheduled")}

    subject = models.CharField(max_length=100, help_text="Enter an email subject")

    body = models.TextField(help_text="Enter the message body")

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    time_scheduled = models.DateTimeField(
        default=timezone.now, auto_now_add=False, blank=True
    )
    time_sent = models.DateTimeField(
        default=timezone.now, auto_now_add=False, blank=True
    )

    last_update = models.DateTimeField(auto_now_add=True, blank=True)

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="emails"
    )

    def __str__(self):
        """String for representing the Email Model"""
        return self.subject
