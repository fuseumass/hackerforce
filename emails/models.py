from django.db import models

# Create your models here.

class Email(models.Model):
    """Object representing the Contact."""

    subject = models.CharField(
        max_length=100, help_text="Enter an email subject"
    )

    messageText = models.TextField(
        help_text="Enter the message body"
    )

    messageStatus = models.CharField(
        max_length=50, help_text="Draft, Outbox, or Sent"
    )

    lastUpdate = models.DateTimeField(auto_now_add=True, blank=True)

    modifiedBy = models.CharField(
        max_length=50, help_text="Enter your username"
    )

    checkBox = models.BooleanField(default=False)

    def __str__(self):
        """String for representing the Email Model"""
        return self.subject