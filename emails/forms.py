from django import forms
from emails.models import Email
from datetime import datetime

class EmailForm(forms.ModelForm):

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
        widget=forms.Textarea(
            attrs={
                "rows":"10",
                "class": "form-control",
                "placeholder": "Message Body",
            } 
        ),
    ) 

    time_scheduled = forms.DateTimeField(
        required = False,
        widget=forms.DateTimeInput(
            attrs={
                "class":"form-control",
                # "type":"datetime-local",
                "data-mask":"mm/dd/yy hh:mm",
                "placeholder":"mm/dd/yy hh:mm"
            }
        )
    ) 

    class Meta:
        model = Email
        fields = ('subject', 'body', 'time_scheduled')