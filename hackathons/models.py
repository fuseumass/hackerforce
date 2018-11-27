from django.db import models

from companies.models import Company


class Tier(models.Model):
    name = models.CharField(max_length=100)


class Perk(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)


class Hackathon(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField(blank=True)
    fundraising_goal = models.IntegerField(blank=True)
    tiers = models.ManyToManyField(Tier, null=True, blank=True)
    perks = models.ManyToManyField(Perk, null=True, blank=True)


class Sponsorship(models.Model):
    STATUSES = (
        ("uncontacted", "Uncontacted"),
        ("contacted", "Contacted"),
        ("donated", "Donated"),
    )

    hackathon = models.ForeignKey(
        Hackathon, on_delete=models.CASCADE, related_name="sponsorships"
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="sponsorships"
    )

    contribution = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUSES)

    tier = models.ForeignKey(
        Tier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sponsorships",
    )
    perks = models.ManyToManyField(Perk, null=True, blank=True)

