from django import forms
from multiselectfield import MultiSelectFormField
from emails.models import Email
from companies.models import Company, Industry
from contacts.models import Contact
from ckeditor.widgets import CKEditorWidget

from shared.fields import GroupedModelMultiChoiceField

class ComposeFromContactsForm(forms.ModelForm):

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
        max_length=50,
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
        fields = ('to_contacts', 'subject', 'body')

class ComposeFromCompanyForm(forms.ModelForm):

    to_companies = forms.ModelMultipleChoiceField(
        required=True,
        queryset=Company.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "class": "col-sm-10",
            }
        ),
    )

    primary_selection = MultiSelectFormField(
        required=True,
        choices=(Email.PRIMARY_CHOICES),
        widget=forms.SelectMultiple(
            attrs={"class": "custom-select col-md-6 col-lg-4", "placeholder": "To Whom?"}
        ),
    )

    contacted_selection = MultiSelectFormField(
        required=True,
        choices=(Email.CONTACTED_CHOICES),
        widget=forms.SelectMultiple(
            attrs={"class": "custom-select col-md-6 col-lg-4", "placeholder": "To Whom?"}
        ),
    )

    subject = forms.CharField(
        max_length=50,
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
        fields = ('to_companies', 'primary_selection', 'contacted_selection', 'subject', 'body')

class ComposeFromIndustryForm(forms.ModelForm):

    to_industries = forms.ModelMultipleChoiceField(
        required=True,
        queryset=Industry.objects.all(),
        widget=forms.SelectMultiple(
            attrs={
                "class": "col-sm-10",
            }
        ),
    )

    size_selection = MultiSelectFormField(
        required=True,
        choices=(Email.SIZE_CHOICES),
        widget=forms.SelectMultiple(
            attrs={"class": "custom-select col-md-6 col-lg-4", "placeholder": "To Whom?"}
        ),
    )

    primary_selection = MultiSelectFormField(
        required=True,
        choices=(Email.PRIMARY_CHOICES),
        widget=forms.SelectMultiple(
            attrs={"class": "custom-select col-md-6 col-lg-4", "placeholder": "To Whom?"}
        ),
    )

    contacted_selection = MultiSelectFormField(
        required=True,
        choices=(Email.CONTACTED_CHOICES),
        widget=forms.SelectMultiple(
            attrs={"class": "custom-select col-md-6 col-lg-4", "placeholder": "To Whom?"}
        ),
    )

    subject = forms.CharField(
        max_length=50,
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
        fields = ('to_industries', 'size_selection', 'primary_selection', 'contacted_selection', 'subject', 'body')
