from django.db import models

from companies.models import Company


class Hackathon(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField(blank=True)
    fundraising_goal = models.IntegerField(blank=True)


class Tier(models.Model):
    name = models.CharField(max_length=100)

    hackathon = models.ForeignKey(
        Hackathon, on_delete=models.CASCADE, related_name="tiers"
    )


class Perk(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    hackathon = models.ForeignKey(
        Hackathon, on_delete=models.CASCADE, related_name="perks"
    )


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

    tier = models.ManyToManyField(Tier, blank=True)
    perks = models.ManyToManyField(Perk, blank=True)

