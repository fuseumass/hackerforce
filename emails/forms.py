from django import forms
from emails.models import Email

class EmailForm(forms.ModelForm):

    subject = forms.CharField( 
        max_length=50, 
        required=True, 
        widget=forms.TextInput( 
            attrs={  
                "class": "form-control col-md-6 col-lg-4", 
                "placeholder": "Subject", 
            } 
        ), 
    ) 

    messageText = forms.CharField( 
        required=True, 
        widget=forms.TextInput( 
            attrs={  
                "class": "form-control col-md-6 col-lg-4", 
                "placeholder": "Message Body", 
            } 
        ), 
    ) 

    class Meta:
        model = Email
        fields = ('subject', 'messageText')