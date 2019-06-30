from django import forms

from ckeditor.widgets import CKEditorWidget
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
            attrs={"class": "form-control col-md-6 col-lg-4", "placeholder": "Donated", "type": "currency", "step": 0.01}
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
        widget=forms.Textarea(
            attrs={"class": "form-control col-md-6 col-lg-4", "placeholder": "Location", "rows": 3}
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
    notes = forms.CharField(
        required=False,
        widget=CKEditorWidget(
            config_name = 'default',
            attrs={"placeholder": "Notes"}
        ),
    )

    class Meta:
        model = Company
        fields = ("name", "donated", "industries", "location", "status", "size", "notes")
