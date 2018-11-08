from django.db import models
from contacts.models import Contact
# Create your models here.

class Industry(models.Model):
    title = models.CharField(max_length = 20)

class Company(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 140, help_text='enter a company name (e.g. "Amazon")')
    donated = models.IntegerField()
    INDUSTRIES = ((0, 'Web'),(4, 'Data'),(1,'ML'), (2,'Software'), (3, 'Systems'))
    industry = models.IntegerField(default = 0, choices = INDUSTRIES)
    STATUSES = (('U', 'Uncontacted'), ('C', 'Contacted'), ('D', 'Donated'))
    status = models.CharField(max_length = 1, choices = STATUSES)
    SIZES = (('L','Large'),('M', 'Medium'),('S', 'Small'))
    size = models.CharField(max_length = 1, choices = SIZES)
    updated = models.DateField()
    contact = models.CharField(max_length = 140)
    history = None
    def __str__(self):
        return self.name
