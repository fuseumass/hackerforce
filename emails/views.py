from django.shortcuts import render, redirect, get_object_or_404
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

            if "send_message" in request.POST:
                email.status = "sent"
            elif "schedule_message" in request.POST:
                email.status = "scheduled"
            elif "save_draft" in request.POST:
                email.status = "draft"
            
            email.to.set(form.cleaned_data["to"])
            email.save()
        else:
            print("Form is invalid")
            for error in form.errors:
                print(error)
    else:
        form = EmailForm()
    return render(request, "emails.html", {"form": form})

@login_required
def drafts(request):
    emails = Email.objects.filter(status="draft")
    return render(request, "drafts.html", {"emails": emails})

@login_required
def sent(request):
    emails = Email.objects.filter(status="sent")
    return render(request, "sent.html", {"emails": emails})

@login_required
def outbox(request):
    emails = Email.objects.filter(status="scheduled")
    return render(request, "outbox.html", {"emails": emails})

@login_required
def email_edit(request, pk):
    email = get_object_or_404(Email, pk=pk)
    if request.method == "POST":
        form = EmailForm(request.POST, instance=email)
        if form.is_valid():
            email = form.save(commit=False)
            email.to.set(form.cleaned_data["to"])
            if "send_message" in request.POST:
                email.status = "sent"
                email.save()
                return redirect("emails:sent")
            elif "schedule_message" in request.POST:
                email.status = "scheduled"
                email.save()
                return redirect("emails:outbox")
            elif "save_draft" in request.POST:
                email.status = "draft"
                email.save()
                return redirect("emails:drafts")
    else:
        form = EmailForm(instance=email)
    return render(request, "emails_edit.html", {"form": form})

@login_required
def sent_view(request, pk):
    email = get_object_or_404(Email, pk=pk)
    if request.method == "POST":
        return redirect("emails:sent")

    else:
        form = EmailForm(instance=email)
    return render(request, "sent_view.html", {"form": form})
