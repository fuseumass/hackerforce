from django.db import models
from django.db.models import Q
from django.utils import timezone
from multiselectfield import MultiSelectField

from companies.models import Company, Industry
from profiles.models import User
from contacts.models import Contact
from hackathons.models import Hackathon, Lead

class Email(models.Model):
    """Object representing an Email."""
    STATUS_CHOICES = [("sent", "Sent"), ("draft", "Draft"), ("scheduled", "Scheduled")]
    CONTACTED_CHOICES = [("U", "Uncontacted"), ("C1", "Contacted 1x"), ("C2", "Contacted 2x"), ("C3", "Contacted 3x or more")]
    SIZE_CHOICES = [("S", "Small"), ("M", "Medium"), ("L", "Large")]
    PRIMARY_CHOICES = [("P", "Primary"), ("NP", "Not-Primary")]

    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name="emails")

    to_companies = models.ManyToManyField(Company, blank=True, related_name="email_templates")
    to_contacts = models.ManyToManyField(Contact, blank=True, related_name="email_templates")
    to_industries = models.ManyToManyField(Industry, blank=True)
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

    FROM_CONTACTS = "FROM_CONTACTS"
    FROM_COMPANY = "FROM_COMPANY"
    FROM_INDUSTRY = "FROM_INDUSTRY"
    @property
    def email_type(self):
        if self.to_contacts.count():
            return self.FROM_CONTACTS
        elif self.to_companies.count():
            return self.FROM_COMPANY
        else:
            return self.FROM_INDUSTRY

    def get_leads_and_contacts(self):
        if self.email_type == self.FROM_CONTACTS:
            leads = Lead.objects.filter(contacts__in=self.to_contacts.all(), sponsorship__hackathon=self.hackathon)
            without_leads = self.to_contacts.exclude(leads__sponsorship__hackathon=self.hackathon)
            return leads, without_leads
        elif self.email_type == self.FROM_COMPANY:
            primary = [True if s == 'P' else False for s in self.primary_selection]

            times_contacted = Q(times_contacted=-1)
            contacted_zero_times = False
            contacted_1plus_times = False
            for c in self.contacted_selection:
                if c == 'U':
                    contacted_zero_times = True
                else:
                    contacted_1plus_times = True
                if c == 'C1':
                    times_contacted.add(Q(times_contacted=1), Q.OR)
                elif c == 'C2':
                    times_contacted.add(Q(times_contacted=2), Q.OR)
                elif c == 'C3':
                    times_contacted.add(Q(times_contacted__geq=3), Q.OR)

            if not contacted_zero_times and not contacted_1plus_times:
                times_contacted = Q()

            leads = Lead.objects.filter((Q(sponsorship__hackathon=self.hackathon) & \
                Q(contact__company__in=self.to_companies.all()) & \
                times_contacted & \
                Q(contact__primary__in=primary)))
            
            
            without_leads = Contact.objects.none()
            if contacted_zero_times:
                without_leads = Contact.objects.exclude(leads__sponsorship__hackathon=self.hackathon).filter(
                    Q(company__in=self.to_companies.all()) & \
                    Q(primary__in=primary))
            
            return leads, without_leads
        elif self.email_type == self.FROM_INDUSTRY:
            primary = [True if s == 'P' else False for s in self.primary_selection]

            times_contacted = Q(times_contacted=-1)
            contacted_zero_times = False
            contacted_1plus_times = False
            for c in self.contacted_selection:
                if c == 'U':
                    contacted_zero_times = True
                else:
                    contacted_1plus_times = True
                if c == 'C1':
                    times_contacted.add(Q(times_contacted=1), Q.OR)
                elif c == 'C2':
                    times_contacted.add(Q(times_contacted=2), Q.OR)
                elif c == 'C3':
                    times_contacted.add(Q(times_contacted__geq=3), Q.OR)

            if not contacted_zero_times and not contacted_1plus_times:
                times_contacted = Q()

            leads = Lead.objects.filter(Q(sponsorship__hackathon=self.hackathon) & (
                times_contacted | \
                Q(contact__company__industries__in=self.to_industries.all()) | \
                Q(contact__company__size__in=self.size_selection) | \
                Q(contact__primary__in=primary)))
            
            without_leads = Contact.objects.none()
            if contacted_zero_times:
                without_leads = Contact.objects.exclude(leads__sponsorship__hackathon=self.hackathon).filter(
                    company__industries__in=self.to_industries.all(),
                    company__size__in=self.size_selection,
                    primary__in=primary
                )
            
            return leads, without_leads

    def __str__(self):
        """String for representing the Email Model"""
        return self.subject
