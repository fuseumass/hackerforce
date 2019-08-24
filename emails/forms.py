from django import forms
from multiselectfield import MultiSelectFormField
from emails.models import Email
from companies.models import Company, Industry
from contacts.models import Contact
from ckeditor.widgets import CKEditorWidget

from shared.fields import GroupedModelMultiChoiceField

class ComposeBaseForm(forms.ModelForm):
    internal_title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Internal Title",
            }
        )
    )

    subject = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Subject",
            }
        ),
    )

    body = forms.CharField(
        required=True,
        widget=CKEditorWidget(
            config_name = 'default',
            attrs={"placeholder": "Body"}
        ),
    )

    attach_packet = forms.BooleanField(required=False)

    class Meta:
        model = Email
        fields = ('internal_title', 'subject', 'body', 'attach_packet',)


class ComposeFromContactsForm(ComposeBaseForm):
    to_contacts = GroupedModelMultiChoiceField(
        required=True,
        queryset=Contact.objects.order_by("company"),
        group_by_field='company',
        widget=forms.SelectMultiple(
            attrs={
                "class": "col-sm-10",
            }
        ),
    )

    subject = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Subject",
            }
        ),
    )

    body = forms.CharField(
        required=True,
        widget=CKEditorWidget(
            config_name = 'default',
            attrs={"placeholder": "Body"}
        ),
    )

    status = "draft"


    class Meta:
        model = Email
        fields = ('internal_title', 'to_contacts', 'subject', 'body', 'attach_packet',)

class ComposeFromCompanyForm(forms.ModelForm):
    to_companies = forms.ModelMultipleChoiceField(
        label="Send to:",
        help_text="Contacts from these companies",
        required=True,
        queryset=Company.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "class": "col-sm-10",
                "placeholder": "Companies list",
            }
        ),
    )

    primary_selection = MultiSelectFormField(
        label="Which are:",
        help_text="Primary status (ignored if unset)",
        required=False,
        choices=(Email.PRIMARY_CHOICES),
        widget=forms.SelectMultiple(
            attrs={"class": "custom-select col-md-6 col-lg-4", "placeholder": ""}
        ),
    )

    contacted_selection = MultiSelectFormField(
        label="With contacts who have been:",
        help_text="Contacted this many times (ignored if unset)",
        required=False,
        choices=(Email.CONTACTED_CHOICES),
        widget=forms.SelectMultiple(
            attrs={"class": "custom-select col-md-6 col-lg-4", "placeholder": ""}
        ),
    )

    exclude_contacted_companies = forms.BooleanField(required=False)

    subject = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Subject",
            }
        ),
    )

    body = forms.CharField(
        required=True,
        widget=CKEditorWidget(
            config_name = 'default',
            attrs={"placeholder": "Body"}
        ),
    )

    class Meta:
        model = Email
        fields = ('internal_title', 'to_companies', 'primary_selection', 'contacted_selection', 'exclude_contacted_companies', 'subject', 'body', 'attach_packet',)

class ComposeFromIndustryForm(ComposeBaseForm):
    to_industries = forms.ModelMultipleChoiceField(
        label="With industries:",
        help_text="Company industries (ignored if unset) AND",
        required=False,
        queryset=Industry.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "class": "col-sm-10",
            }
        ),
    )

    size_selection = MultiSelectFormField(
        label="With size:",
        help_text="Company size (ignored if unset) AND",
        required=False,
        choices=(Email.SIZE_CHOICES),
        widget=forms.SelectMultiple(
            attrs={"class": "custom-select col-md-6 col-lg-4", "placeholder": "To Whom?"}
        ),
    )

    primary_selection = MultiSelectFormField(
        label="Which are:",
        help_text="Primary status (ignored if unset) AND",
        required=False,
        choices=(Email.PRIMARY_CHOICES),
        widget=forms.SelectMultiple(
            attrs={"class": "custom-select col-md-6 col-lg-4", "placeholder": "To Whom?"}
        ),
    )

    contacted_selection = MultiSelectFormField(
        label="With contacts which have been:",
        help_text="Contacted this many times (ignored if unset)",
        required=False,
        choices=(Email.CONTACTED_CHOICES),
        widget=forms.SelectMultiple(
            attrs={"class": "custom-select col-md-6 col-lg-4", "placeholder": "To Whom?"}
        ),
    )

    exclude_contacted_companies = forms.BooleanField(required=False)

    subject = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Subject",
            }
        ),
    )

    body = forms.CharField(
        required=True,
        widget=CKEditorWidget(
            config_name = 'default',
            attrs={"placeholder": "Body"}
        ),
    )

    class Meta:
        model = Email
        fields = ('internal_title', 'to_industries', 'size_selection', 'primary_selection', 'contacted_selection', 'exclude_contacted_companies', 'subject', 'body', 'attach_packet',)

class EmailChangeTypeForm(forms.Form):
    TYPE_CHOICES = ((Email.FROM_CONTACTS, "From contacts"), (Email.FROM_COMPANY, "From company"), (Email.FROM_INDUSTRY, "From industry"))
    new_type = forms.ChoiceField(choices=TYPE_CHOICES)

    class Meta:
        fields = ('new_type',)