from django import forms
from .models import Company, Industry


class CompanyForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control col-md-6 col-lg-4", "placeholder": "Name"}
        ),
    )
    donated = forms.IntegerField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control col-md-6 col-lg-4", "placeholder": "Donated"}
        ),
    )
    industries = forms.ModelMultipleChoiceField(
        required=True,
        queryset=Industry.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "custom-select col-md-6 col-lg-4"}),
    )
    location = forms.CharField(
        max_length=140,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control col-md-6 col-lg-4", "placeholder": "Location"}
        ),
    )
    status = forms.ChoiceField(
        required=True,
        choices=(Company.STATUSES),
        widget=forms.Select(
            attrs={"class": "custom-select col-md-6 col-lg-4", "placeholder": "Status"}
        ),
    )
    size = forms.ChoiceField(
        required=True,
        choices=(Company.SIZES),
        widget=forms.Select(
            attrs={"class": "custom-select col-md-6 col-lg-4", "placeholder": "Size"}
        ),
    )

    class Meta:
        model = Company
        fields = ("name", "donated", "industries", "location", "status", "size")
