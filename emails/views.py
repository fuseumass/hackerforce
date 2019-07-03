from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from hackathons.models import Hackathon
from .models import Email
from .forms import Compose1

# Create your views here.
def emails(request, h_pk):
  hackathon = get_object_or_404(Hackathon, pk=h_pk)
  return render(request, "email_compose.html", {"h" : hackathon})

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

def sent(request, h_pk):
  return render(request, "email_sent.html")

def compose1(request, h_pk):
  hackathon = get_object_or_404(Hackathon, pk=h_pk)
  if request.method == "POST":
    form = Compose1(request.POST)
    if form.is_valid():
      email = form.save(commit=False)
      email.hackathon = hackathon
      email.save()
      messages.success(request, f"Created email with subject: {email.subject}")
      redirect("emails:drafts", h_pk)
  else:
    form = Compose1()
  return render(request, "email_compose1.html", {"form" : form})

def compose2(request, h_pk):
  return render(request, "email_compose2.html")

def compose3(request, h_pk):
  return render(request, "email_compose3.html")
