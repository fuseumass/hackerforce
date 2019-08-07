from django.db import models
from django.db.models import Q
from django.template import Template, Context
from django.utils import timezone

from shared.forms.fields import MultiSelectField
from companies.models import Company, Industry
from profiles.models import User
from contacts.models import Contact
from hackathons.models import Hackathon, Lead, Sponsorship

class Email(models.Model):
    """Object representing an Email."""
    STATUS_CHOICES = [("sent", "Sent"), ("draft", "Draft"), ("scheduled", "Scheduled")]
    SENT = 'sent'
    DRAFT = 'draft'
    SCHEDULED = 'scheduled'
    CONTACTED_CHOICES = [("U", "Uncontacted"), ("C1", "Contacted 1x"), ("C2", "Contacted 2x"), ("C3", "Contacted 3x or more")]
    SIZE_CHOICES = Company.SIZES
    PRIMARY_CHOICES = [("P", "Primary"), ("NP", "Not-Primary")]

    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name="emails")

    to_companies = models.ManyToManyField(Company, blank=True, related_name="email_templates")
    to_contacts = models.ManyToManyField(Contact, blank=True, related_name="email_templates")
    to_industries = models.ManyToManyField(Industry, blank=True)
    contacted_selection = MultiSelectField(max_choices=4, choices=CONTACTED_CHOICES, blank=True)
    size_selection = MultiSelectField(choices=SIZE_CHOICES, max_choices=3, blank=True)
    primary_selection = MultiSelectField(choices=PRIMARY_CHOICES, max_choices=2, blank=True)
    exclude_contacted_companies = models.BooleanField(default=False, help_text="Whether to exclude all contacts from companies who have already been contacted")
    
    internal_title = models.CharField(max_length=200, help_text="Enter an internal title for this email")

    subject = models.CharField(max_length=200, help_text="Enter an email subject")
    body = models.TextField(help_text="Enter the message body")
    attach_packet = models.BooleanField(default=False, help_text="Whether the sponsorship packet should be attached")

    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    sent_contacts = models.ManyToManyField(Contact, blank=True, related_name="emails_sent")

    time_scheduled = models.DateTimeField(blank=True, null=True)
    time_sent = models.DateTimeField(blank=True, null=True)

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
    
    def clear_current_type(self):
        if self.email_type == self.FROM_CONTACTS:
            self.to_contacts.clear()
        elif self.email_type == self.FROM_COMPANY:
            self.to_companies.clear()
            self.primary_selection = None
            self.contacted_selection = None
        elif self.email_type == self.FROM_INDUSTRY:
            self.primary_selection = None
            self.contacted_selection = None
            self.size_selection = None
            self.to_industries.clear()
    
    def populate_settable_m2m_from(self, other):
        for c in other.to_companies.all():
            self.to_companies.add(c)
        for c in other.to_contacts.all():
            self.to_contacts.add(c)
        for i in other.to_industries.all():
            self.to_industries.add(i)

    def _leads_and_contacts_from(self, contacts):
        leads = Lead.objects.filter(contact__in=contacts.all(), sponsorship__hackathon=self.hackathon)
        without_leads = contacts.exclude(leads__sponsorship__hackathon=self.hackathon)
        return leads, without_leads

    def get_leads_and_contacts(self):
        if self.status == Email.SENT:
            # When an email is sent, we persist the contacts which we sent the email
            # to in a new field, and override get_leads_and_contacts.
            return self._leads_and_contacts_from(self.sent_contacts)

        elif self.email_type == self.FROM_CONTACTS:
            # FROM_CONTACTS: Returns the contacts/leads of the specified contacts
            return self._leads_and_contacts_from(self.to_contacts)

        elif self.email_type == self.FROM_COMPANY:
            # FROM_COMPANY: AND of the following inputs:
            #  * companies which were entered (all options OR'd)
            #  * times contacted (all options OR'd, ignored if unset)
            #  * contact's primary status in their company (all options OR'd, ignored if unset)
            primary = [True if s == 'P' else False for s in self.primary_selection]
            if not primary:
                primary = [True, False]

            times_contacted = Q(times_contacted=-1)
            contacted_zero_times = False
            contacted_1plus_times = False
            empty_contacted_field = True
            for c in self.contacted_selection:
                empty_contacted_field = False
                if c == 'U':
                    contacted_zero_times = True
                else:
                    contacted_1plus_times = True
                if c == 'C1':
                    times_contacted.add(Q(times_contacted=1), Q.OR)
                elif c == 'C2':
                    times_contacted.add(Q(times_contacted=2), Q.OR)
                elif c == 'C3':
                    times_contacted.add(Q(times_contacted__gte=3), Q.OR)

            if not contacted_zero_times and not contacted_1plus_times:
                times_contacted = Q()
            
            if empty_contacted_field:
                times_contacted = Q()
            
            if self.exclude_contacted_companies:
                leads = Lead.objects.none()
            else:
                leads = Lead.objects.filter((Q(sponsorship__hackathon=self.hackathon) & \
                    Q(contact__company__in=self.to_companies.all()) & \
                    times_contacted & \
                    Q(contact__primary__in=primary)))
            
            
            without_leads = Contact.objects.none()
            if contacted_zero_times or empty_contacted_field:
                without_leads = Contact.objects.exclude(leads__sponsorship__hackathon=self.hackathon).filter(
                    Q(company__in=self.to_companies.all()) & \
                    Q(primary__in=primary))
                if self.exclude_contacted_companies:
                    contacted_companies_pk = Sponsorship.objects.filter(hackathon=self.hackathon).values_list("company__pk", flat=True)
                    without_leads = without_leads.exclude(company__in=contacted_companies_pk)
            
            return leads, without_leads
        elif self.email_type == self.FROM_INDUSTRY:
            # FROM_INDUSTRY: AND of the following inputs:
            #  * company's industries (all options OR'd, ignored if unset)
            #  * contact's number of times contacted (all options OR'd, ignored if unset)
            #  * contact's primary status in their company (all options OR'd, ignored if unset)
            primary = [True if s == 'P' else False for s in self.primary_selection]
            if not primary:
                primary = [True, False]

            times_contacted = Q(times_contacted=-1)
            contacted_zero_times = False
            contacted_1plus_times = False
            empty_contacted_field = True
            for c in self.contacted_selection:
                empty_contacted_field = False
                if c == 'U':
                    contacted_zero_times = True
                else:
                    contacted_1plus_times = True
                if c == 'C1':
                    times_contacted.add(Q(times_contacted=1), Q.OR)
                elif c == 'C2':
                    times_contacted.add(Q(times_contacted=2), Q.OR)
                elif c == 'C3':
                    times_contacted.add(Q(times_contacted__gte=3), Q.OR)

            if not contacted_zero_times and not contacted_1plus_times:
                times_contacted = Q()
            
            sizes = self.size_selection
            if not sizes:
                sizes = dict(Company.SIZES).keys()

            if self.exclude_contacted_companies:
                leads = Lead.objects.none()
            else:
                leads = Lead.objects.filter(Q(sponsorship__hackathon=self.hackathon) &
                    times_contacted & \
                    Q(contact__company__industries__in=self.to_industries.all()) & \
                    Q(contact__company__size__in=sizes) & \
                    Q(contact__primary__in=primary))
            
            without_leads = Contact.objects.none()
            if contacted_zero_times or empty_contacted_field:
                without_leads = Contact.objects.exclude(leads__sponsorship__hackathon=self.hackathon).filter(
                    Q(company__industries__in=self.to_industries.all()) & \
                    Q(company__size__in=sizes) & \
                    Q(primary__in=primary))
                
                if self.exclude_contacted_companies:
                    contacted_companies_pk = Sponsorship.objects.filter(hackathon=self.hackathon).values_list("company__pk", flat=True)
                    without_leads = without_leads.exclude(company__in=contacted_companies_pk)
            
            return leads, without_leads
    
    def render_body(self, contact=None):
        ctx = Context()
        if contact:
            ctx = Context(self.render_body_context(contact))
        return Template(self.body).render(ctx)
    
    def render_body_context(self, contact):
        return {
            "contact": contact,
            "company": contact.company if contact else None,
        }

    def __str__(self):
        """String for representing the Email Model"""
        return f"{self.internal_title} ({self.subject})"
