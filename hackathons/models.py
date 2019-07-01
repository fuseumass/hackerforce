from django.db import models

from companies.models import Company


class Hackathon(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField(blank=True)
    fundraising_goal = models.IntegerField(blank=True)

    def __str__(self):
        return self.name

    def latest():
        return Hackathon.objects.latest("date")


class Tier(models.Model):
    name = models.CharField(max_length=100)

    hackathon = models.ForeignKey(
        Hackathon, on_delete=models.CASCADE, related_name="tiers"
    )

    def __str__(self):
        return self.name


class Perk(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    hackathon = models.ForeignKey(
        Hackathon, on_delete=models.CASCADE, related_name="perks"
    )

    def __str__(self):
        return self.name


class Sponsorship(models.Model):
    STATUSES = (("pending", "Pending"), ("received", "Recieved"))

    hackathon = models.ForeignKey(
        Hackathon, on_delete=models.CASCADE, related_name="sponsorships"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="sponsorships"
    )
    contribution = models.IntegerField()
    status = models.CharField(max_length=12, choices=STATUSES)
    tier = models.ForeignKey(Tier, related_name="sponsorships", on_delete=models.SET_NULL, null=True)
    perks = models.ManyToManyField(Perk, blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Company: {self.company}, Status: {self.status}, Contribution: {self.contribution}"

"""
class Lead(models.Model):
    STATUSES = (("U", "Uncontacted"), ("C", "Contacted"))
    ROLES = (("N", "None"), ("P", "Primary"))

    sponsorship = models.ForeignKey(
        Sponsorship, on_delete=models.CASCADE, related_name="leads"
    )
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name="leads"
    )

    status = models.CharField(max_length=1, choices=STATUSES)
    role = models.CharField(max_length=1, choices=ROLES)

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Sponsorship: {self.sponsorship}, Contact: {self.contact}, Status: {self.status}, Role: {self.role}"
"""