from django import forms
from emails.models import Email
from datetime import datetime
from companies.models import Company

class EmailForm(forms.ModelForm):

    to = forms.ModelMultipleChoiceField(
        required=True,
        queryset=Company.objects.all(),
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
               # "type":"datetime",
                "class":"form-control",
                # "type":"datetime-local",
                "data-mask":"00/00/0000 00:00:00",
                "placeholder":"mm/dd/yy hh:mm"
            }
        )
    )

    # <input type="datetime-local" name="field-name" class="form-control" data-mask="00/00/0000 00:00:00"
    #                         data-mask-clearifnotmatch="true" placeholder="00/00/0000 00:00:00" />

    status = forms.ChoiceField(choices=[("sent", "Sent"), ("draft", "Draft"), ("scheduled", "Scheduled")], required = False)


    class Meta:
        model = Email
        fields = ('to', 'subject', 'body', 'time_scheduled', 'status')
        #fields = ('subject', 'body', 'time_scheduled', 'status')
