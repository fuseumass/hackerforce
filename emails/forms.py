from django import forms
from multiselectfield import MultiSelectFormField
from emails.models import Email
from companies.models import Company, Industry
from contacts.models import Contact
from ckeditor.widgets import CKEditorWidget

from shared.fields import GroupedModelMultiChoiceField

class ComposeFromContactsForm(forms.ModelForm):

    internal_title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Internal Title",
            }
        )
    )

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
        fields = ('internal_title', 'to_contacts', 'subject', 'body')

class ComposeFromCompanyForm(forms.ModelForm):

    internal_title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Internal Title",
            }
        )
    )

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
        label="Which have been:",
        help_text="Contacted this many times (ignored if unset)",
        required=False,
        choices=(Email.CONTACTED_CHOICES),
        widget=forms.SelectMultiple(
            attrs={"class": "custom-select col-md-6 col-lg-4", "placeholder": ""}
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
        fields = ('internal_title', 'to_companies', 'primary_selection', 'contacted_selection', 'subject', 'body')

class ComposeFromIndustryForm(forms.ModelForm):

    internal_title = forms.CharField(
        help_text="Send emails to contacts at companies which match...",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Internal Title",
            }
        )
    )

    to_industries = forms.ModelMultipleChoiceField(
        label="With industries:",
        help_text="Company industries AND",
        required=True,
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
        label="Which have been:",
        help_text="Contacted status (ignored if unset)",
        required=False,
        choices=(Email.CONTACTED_CHOICES),
        widget=forms.SelectMultiple(
            attrs={"class": "custom-select col-md-6 col-lg-4", "placeholder": "To Whom?"}
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
        fields = ('internal_title', 'to_industries', 'size_selection', 'primary_selection', 'contacted_selection', 'subject', 'body')

class EmailChangeTypeForm(forms.Form):
    TYPE_CHOICES = ((Email.FROM_CONTACTS, "From contacts"), (Email.FROM_COMPANY, "From company"), (Email.FROM_INDUSTRY, "From industry"))
    new_type = forms.ChoiceField(choices=TYPE_CHOICES)

    class Meta:
        fields = ('new_type',)