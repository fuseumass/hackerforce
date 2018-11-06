from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    phone_number = PhoneNumberField(blank=True)
    email = models.EmailField()
    is_warm_contact = models.BooleanField()
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100) # replace with assosciation
    # sponsorships field

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
