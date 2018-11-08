from django import forms
from phonenumber_field.formfields import PhoneNumberField


from .models import Contact
from companies.models import Company


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control col-md-6 col-lg-4",
                "placeholder": "First Name",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control col-md-6 col-lg-4",
                "placeholder": "Last Name",
            }
        ),
    )
    company = forms.ModelChoiceField(
        required=True,
        queryset=Company.objects.all(),
        widget=forms.Select(
            attrs={"class": "custom-select col-md-6 col-lg-4", "placeholder": "Company"}
        ),
    )
    position = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control col-md-6 col-lg-4", "placeholder": "Position"}
        ),
    )
    email = forms.EmailField(
        max_length=50,
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control col-md-6 col-lg-4",
                "placeholder": "example@email.com",
            }
        ),
    )
    phone_number = PhoneNumberField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control col-md-6 col-lg-4",
                "placeholder": "(000) 000-0000",
            }
        ),
    )

    class Meta:
        model = Contact
        fields = (
            "first_name",
            "last_name",
            "company",
            "position",
            "email",
            "phone_number",
            "is_warm_contact",
        )
