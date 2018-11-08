from django.shortcuts import render
from emails.forms import EmailForm


def emails(request):
    form = EmailForm()
    return render(request, 'emails.html.j2', {'form':form})


def drafts(request):
    return render(request, 'drafts.html.j2')


def sent(request):
    return render(request, 'sent.html.j2')


def outbox(request):
    return render(request, 'outbox.html.j2')
