from django import forms
from .models import Company, Industry
from contacts.models import Contact
import datetime

class CompanyForm(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control col-md-6 col-lg-4",
                "placeholder": "Name",
            }
        ),
    )
    donated = forms.IntegerField(
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control col-md-6 col-lg-4", "placeholder": "Donated"}
        ),
    )
    #updated = datetime.datetime.now()
    industries = ("industries")
    location = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control col-md-6 col-lg-4",
                "placeholder": "Location",
            }
        ),
    )
    status = forms.ChoiceField(
        required=True,
        choices=(("U", "Uncontacted"), ("C", "Contacted"), ("D", "Donated")),
        widget=forms.Select(
            attrs={"class": "custom-select col-md-6 col-lg-4", "placeholder": "Status"}
        ),
    )
    size = forms.ChoiceField(
        #required=True,
        choices=(("L", "Large"), ("M", "Medium"), ("S", "Small")),
        widget=forms.Select(
            attrs={"class": "custom-select col-md-6 col-lg-4", "placeholder": "Size"}
        ),
    )
    updated = forms.DateField()

    fields = ("industries")
             
    def __init__(self, *args, **kwargs):
        
        super(CompanyForm, self).__init__(*args, **kwargs)
        
        self.fields["industries"].widget = forms.CheckboxSelectMultiple()
        self.fields["industries"].queryset = Industry.objects.all()
    class Meta:
        model = Company
        fields = (
            "name",
            "donated",
            "industries",
            "location",
            "status",
            "size",
            "updated"
        )
