from django.db import models
from django.utils import timezone
from multiselectfield import MultiSelectField

from companies.models import Company, Industry
from profiles.models import User
from contacts.models import Contact
from hackathons.models import Hackathon

class Email(models.Model):
    """Object representing an Email."""
    STATUS_CHOICES = [("sent", "Sent"), ("draft", "Draft"), ("scheduled", "Scheduled")]
    CONTACTED_CHOICES = [("U", "Uncontacted"), ("C1", "Contacted <= 1"), ("C2", "Contacted <= 2"), ("C0", "Contacted > 0")]
    SIZE_CHOICES = [("S", "Small"), ("M", "Medium"), ("L", "Large")]
    PRIMARY_CHOICES = [("P", "Primary"), ("NP", "Not-Primary")]

    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name="emails")

    to_companies = models.ManyToManyField(Company, blank=True, null=True, related_name="email_templates")
    to_contacts = models.ManyToManyField(Contact, blank=True, null=True, related_name="email_templates")
    to_industries = models.ManyToManyField(Industry, blank=True, null=True)
    contacted_selection = MultiSelectField(max_choices=4, choices=CONTACTED_CHOICES, blank=True)
    size_selection = MultiSelectField(choices=SIZE_CHOICES, max_choices=3, blank=True)
    primary_selection = MultiSelectField(choices=PRIMARY_CHOICES, max_choices=2, blank=True)

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
        User, on_delete=models.SET_NULL, related_name="emails", null=True
    )

    def __str__(self):
        """String for representing the Email Model"""
        return self.subject
