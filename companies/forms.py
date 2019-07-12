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
    industries = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Industry.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "custom-select col-md-6 col-lg-4"}),
    )
    location = forms.CharField(
        max_length=140,
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-control col-md-6 col-lg-4", "placeholder": "Location", "rows": 3}
        ),
    )
    size = forms.ChoiceField(
        required=False,
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
        fields = ("name", "industries", "location", "size", "notes")
