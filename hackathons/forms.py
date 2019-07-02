from django import forms

from .models import Tier, Perk, Hackathon, Sponsorship
from companies.models import Company
from ckeditor.widgets import CKEditorWidget

class HackathonForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control col-md-6 col-lg-4", "placeholder": "Name"}
        ),
    )

    date = forms.DateField(
        widget=forms.SelectDateWidget(
            attrs={"class": "form-control cold-md-6 cold-lg-4"}
        )
    )

    fundraising_goal = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control cold-md-6 cold-lg-4"})
    )

    class Meta:
        model = Hackathon
        fields = ("name", "date", "fundraising_goal")


class TierForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control col-md-6 col-lg-4", "placeholder": "Name"}
        ),
    )

    hackathon = forms.ModelChoiceField(
        required=True,
        queryset=Hackathon.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "custom-select col-md-6 col-lg-4",
                "placeholder": "Hackathon",
            }
        ),
    )

    class Meta:
        model = Tier
        fields = ("name", "hackathon")


class PerkForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control col-md-6 col-lg-4", "placeholder": "Name"}
        ),
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control col-md-9 col-lg-6",
                "placeholder": "Description",
            }
        ),
    )

    hackathon = forms.ModelChoiceField(
        required=True,
        queryset=Hackathon.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "custom-select col-md-6 col-lg-4",
                "placeholder": "Hackathon",
            }
        ),
    )

    class Meta:
        model = Perk
        fields = ("name", "description", "hackathon")


class SponsorshipForm(forms.ModelForm):
    hackathon = forms.ModelChoiceField(
        required=True,
        queryset=Hackathon.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "custom-select col-md-6 col-lg-4",
                "placeholder": "Hackathon",
            }
        ),
    )

    company = forms.ModelChoiceField(
        required=True,
        queryset=Company.objects.all(),
        widget=forms.Select(
            attrs={"class": "custom-select col-md-6 col-lg-4",}
        ),
    )

    contribution = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control cold-md-6 cold-lg-4", "placeholder": 0}
        )
    )

    def clean_contribution(self):
        contribution = self.cleaned_data.get('contribution')
        return contribution or 0

    status = forms.ChoiceField(
        required=True,
        choices=Sponsorship.STATUSES,
        widget=forms.Select(
            attrs={"class": "custom-select col-md-6 col-lg-4",}
        ),
    )

    tier = forms.ModelChoiceField(
        required=False,
        queryset=Tier.objects.all(),
        widget=forms.Select(attrs={"class": "custom-select col-md-6 col-lg-4",}),
    )

    perks = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Perk.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "custom-select col-md-6 col-lg-4"}),
    )

    notes = forms.CharField(
        required=False,
        widget=CKEditorWidget(
            config_name = 'default',
            attrs={"placeholder": "Notes"}
        ),
    )

    class Meta:
        model = Sponsorship
        fields = ("hackathon", "company", "contribution", "status", "tier", "perks", "notes")

