from django.db import models
from django.core.exceptions import ValidationError

from companies.models import Company
from contacts.models import Contact

class Hackathon(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField(blank=True)
    fundraising_goal = models.IntegerField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def latest():
        try:
            return Hackathon.objects.latest("date")
        except Exception:
            return None
    
    class Meta:
        ordering = ('name',)


class Tier(models.Model):
    name = models.CharField(max_length=100)

    hackathon = models.ForeignKey(
        Hackathon, on_delete=models.CASCADE, related_name="tiers"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)


class Perk(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    hackathon = models.ForeignKey(
        Hackathon, on_delete=models.CASCADE, related_name="perks"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)


class Sponsorship(models.Model):
    ASSIGNED = "assigned"
    CONTACTED = "contacted"
    RESPONDED = "responded"
    CONFIRMED = "confirmed"
    DENIED = "denied"
    GHOSTED = "ghosted"
    PAID = "paid"
    STATUSES = (
        (ASSIGNED, "Assigned"),
        (CONTACTED, "Contacted"),
        (RESPONDED, "Responded"),
        (CONFIRMED, "Confirmed"),
        (DENIED, "Denied"),
        (GHOSTED, "Ghosted"),
        (PAID, "Paid"),
    )

    hackathon = models.ForeignKey(
        Hackathon, on_delete=models.CASCADE, related_name="sponsorships"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="sponsorships"
    )
    contribution = models.IntegerField(blank=True, default=0)
    status = models.CharField(max_length=20, choices=STATUSES, default=CONTACTED)
    tier = models.ForeignKey(Tier, related_name="sponsorships", on_delete=models.SET_NULL, null=True)
    perks = models.ManyToManyField(Perk, blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.tier and self.tier.hackathon != self.hackathon:
            raise ValidationError(f"Tier {self.tier} is not valid for hackathon {self.hackathon}")
        # Perks can only be checked in the form.


    class Meta:
        unique_together = ('hackathon', 'company',)
        ordering = ('company__name', 'hackathon__name')

    def __str__(self):
        return f"{self.company} for {self.hackathon}"

class Lead(models.Model):
    CONTACTED = "contacted"
    GHOSTED = "ghosted"
    RESPONDED = "responded"
    STATUSES = ((CONTACTED, "Contacted"), (GHOSTED, "Ghosted"), (RESPONDED, "Responded"))
    NO_ROLE = "no_role"
    PRIMARY = "primary"
    ROLES = ((NO_ROLE, "None"), (PRIMARY, "Primary"))

    sponsorship = models.ForeignKey(
        Sponsorship, on_delete=models.CASCADE, related_name="leads"
    )
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name="leads"
    )

    status = models.CharField(max_length=20, choices=STATUSES, default=CONTACTED)
    role = models.CharField(max_length=20, choices=ROLES)

    times_contacted = models.IntegerField(blank=True, default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sponsorship', 'contact',)
        ordering = ('contact__name', 'contact__company__name')

    def status_pretty(self):
        return dict(self.STATUSES)[self.status]

    def role_pretty(self):
        return dict(self.ROLES)[self.role]

    def __str__(self):
        return f"{self.contact} for {self.sponsorship.hackathon}"

    
    def clean(self):
        if self.contact.company != self.sponsorship.company:
            raise ValidationError(f"Contact {self.contact} is not a member of this company: {self.sponsorship}")
        if not self.times_contacted:
            self.times_contacted = 1

