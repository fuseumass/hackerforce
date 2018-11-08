from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from companies.models import Company


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)

    email = models.EmailField()
    phone_number = PhoneNumberField(blank=True)
    is_warm_contact = models.BooleanField()
    # sponsorships field

    def __str__(self):
        return f"Name: {self.name()}, Company: {self.company}, Position: {self.position}, Email: {self.email}, Phone: {self.phone_number}, Warm?: {self.is_warm_contact}"

    def name(self):
        return f"{self.first_name} {self.last_name}"
