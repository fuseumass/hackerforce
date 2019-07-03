from django import forms
from emails.models import Email
from contacts.models import Contact
from ckeditor.widgets import CKEditorWidget

class Compose1(forms.ModelForm):

    to_contacts = forms.ModelMultipleChoiceField(
        required=True,
        queryset=Contact.objects.all(),
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