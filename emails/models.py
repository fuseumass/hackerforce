from django.db import models
from datetime import datetime

from profiles.models import User


class Email(models.Model):
    """Object representing the Contact."""

    subject = models.CharField(max_length=100, help_text="Enter an email subject")

    message_text = models.TextField(help_text="Enter the message body")

    message_status = models.CharField(max_length=50, help_text="Draft, Outbox, or Sent")

    time_scheduled = models.DateTimeField(
        default=datetime.now(), auto_now_add=False, blank=True
    )

    last_update = models.DateTimeField(auto_now_add=True, blank=True)

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="emails"
    )

    check_box = models.BooleanField(default=False)

    def __str__(self):
        """String for representing the Email Model"""
        return self.subject
