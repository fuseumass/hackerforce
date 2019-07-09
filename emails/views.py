from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from hackathons.models import Hackathon
from .models import Email
from .forms import Compose1, Compose2, Compose3

# Create your views here.
@login_required
def emails(request, h_pk):
  hackathon = get_object_or_404(Hackathon, pk=h_pk)
  return render(request, "email_compose.html", {"h" : hackathon})

@login_required
def email_detail(request, h_pk, pk):
  email = get_object_or_404(Email, pk=pk)
  hackathon = get_object_or_404(Hackathon, pk=h_pk)
  return render(request, "email_detail_view.html", {"email": email, "hackathon": hackathon})

@login_required
def drafts(request, h_pk):
  hackathon = get_object_or_404(Hackathon, pk=h_pk)
  emails = Email.objects.filter(hackathon=hackathon)

  order_by = request.GET.get("order_by")
  if order_by:
    emails = emails.order_by(*order_by.split(","))

  paginator = Paginator(emails, 25)
  page = request.GET.get("page")
  emails = paginator.get_page(page)
  return render(request, "email_drafts.html", {"emails" : emails})

@login_required
def sent(request, h_pk):
  return render(request, "email_sent.html")

@login_required
def compose1(request, h_pk):
  hackathon = get_object_or_404(Hackathon, pk=h_pk)
  if request.method == "POST":
    form = Compose1(request.POST)
    if form.is_valid():
      email = form.save(commit=False)
      email.hackathon = hackathon
      email.status = 'draft'
      email.save()
      email.to_contacts.set(form.cleaned_data["to_contacts"])
      email.save()
      messages.success(request, f"Created email with subject: {email.subject}")
      return redirect("emails:drafts", h_pk=h_pk)
  else:
    form = Compose1()
  return render(request, "email_compose1.html", {"form" : form})

@login_required
def compose2(request, h_pk):
  hackathon = get_object_or_404(Hackathon, pk=h_pk)
  if request.method == "POST":
    form = Compose2(request.POST)
    if form.is_valid():
      email = form.save(commit=False)
      email.hackathon = hackathon
      email.status = 'draft'
      email.save()
      email.to_companies.set(form.cleaned_data["to_companies"])
      email.save()
      messages.success(request, f"Created email with subject: {email.subject}")
      return redirect("emails:drafts", h_pk=h_pk)
  else:
    form = Compose2()
  return render(request, "email_compose2.html", {"form": form})

@login_required
def compose3(request, h_pk):
  hackathon = get_object_or_404(Hackathon, pk=h_pk)
  if request.method == "POST":
    form = Compose3(request.POST)
    if form.is_valid():
      email = form.save(commit=False)
      email.hackathon = hackathon
      email.status = 'draft'
      email.save()
      email.to_industries.set(form.cleaned_data["to_industries"])
      email.save()
      messages.success(request, f"Created email with subject: {email.subject}")
      return redirect("emails:drafts", h_pk=h_pk)
  else:
    form = Compose3()
  return render(request, "email_compose3.html", {"form": form})
