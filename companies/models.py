from django.db import models

# Create your models here.


class Industry(models.Model):
    COLORS = (
        ("blue", "blue"),
        ("green", "green"),
        ("purple", "purple"),
        ("orange", "orange"),
        ("yellow", "yellow"),
        ("red", "red"),
        ("brown", "brown"),
        ("pink", "pink"),
    )  # temp hack to color tags

    name = models.CharField(max_length=20)
    color = models.CharField(max_length=10, choices=COLORS)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('name',)


class Company(models.Model):
    SIZES = (("L", "Large"), ("M", "Medium"), ("S", "Small"), ("U", "Unknown"))

    name = models.CharField(
        max_length=140, help_text='enter a company name (e.g. "Amazon")'
    )
    industries = models.ManyToManyField(Industry, blank=True)
    location = models.CharField(max_length=140, blank=True)
    size = models.CharField(max_length=1, choices=SIZES)
    notes = models.TextField(blank=True)
    updated = models.DateField(auto_now=True)

    # A special bool for emails
    # if true, this company won't get selected by the blast email selections
    # you can still email them by selecting them manually
    email_exclude = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)