from django.shortcuts import render
from emails.forms import EmailForm
from emails.models import Email
from django.contrib.auth.decorators import login_required

@login_required
def emails(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            email=form.save(commit=False)
            email.created_by=request.user
            email.save()
        else:
            print("Form is invalid")
    else:
        form = EmailForm()
    return render(request, "emails.html.j2", {"form": form})


def drafts(request):
    emails = Email.objects.filter(status="draft")
    return render(request, "drafts.html.j2", {"emails": emails})


def sent(request):
    emails = Email.objects.filter(status="sent")
    return render(request, "sent.html.j2", {"emails": emails})


def outbox(request):
    emails = Email.objects.filter(status="scheduled")
    return render(request, "outbox.html.j2", {"emails": emails})
