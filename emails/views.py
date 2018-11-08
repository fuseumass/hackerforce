from django.shortcuts import render
from emails.forms import EmailForm
from emails.models import Email


def emails(request):

    if request.method=="POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            form.save()
        else:
            print("Form is invalid")
    else:
        form = EmailForm()
    return render(request, 'emails.html.j2', {'form':form})


def drafts(request):
    drafts = Email.objects.all()
    return render(request, 'drafts.html.j2', {"drafts":drafts})


def sent(request):
    return render(request, 'sent.html.j2')


def outbox(request):
    return render(request, 'outbox.html.j2')
