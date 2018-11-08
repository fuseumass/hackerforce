from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    company = models.CharField(max_length=100)  # replace with assosciation
    position = models.CharField(max_length=100)

    email = models.EmailField()
    phone_number = PhoneNumberField(blank=True)
    is_warm_contact = models.BooleanField()
    # sponsorships field

    def name(self):
        return f"{self.first_name} {self.last_name}"
