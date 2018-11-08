from django.db import models

# Create your models here.


class Industry(models.Model):
    COLORS = (
        ("blue", "blue"),
        ("green", "green"),
        ("purple", "purple"),
        ("orange", "orange"),
        ("yellow", "yellow"),
    )  # temp hack to color tags

    name = models.CharField(max_length=20)
    color = models.CharField(max_length=10, choices=COLORS)

    def __str__(self):
        return self.name


class Company(models.Model):
    STATUSES = (("U", "Uncontacted"), ("C", "Contacted"), ("D", "Donated"))
    SIZES = (("L", "Large"), ("M", "Medium"), ("S", "Small"))

    name = models.CharField(
        max_length=140, help_text='enter a company name (e.g. "Amazon")'
    )
    donated = models.IntegerField()
    industries = models.ManyToManyField(Industry)
    location = models.CharField(max_length=140, blank=True)
    status = models.CharField(max_length=1, choices=STATUSES)
    size = models.CharField(max_length=1, choices=SIZES)
    updated = models.DateField()

    def __str__(self):
        return self.name
