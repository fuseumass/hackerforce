from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from companies.models import Company
from hackathons.models import Hackathon
from hackathons.views.sponsorships import combine_lead_and_contacts

from .models import Email
from .forms import ComposeFromContactsForm, ComposeFromCompanyForm, ComposeFromIndustryForm

# Create your views here.
@login_required
def emails(request, h_pk):
  hackathon = get_object_or_404(Hackathon, pk=h_pk)
  return render(request, "email_compose.html", {})

@login_required
def email_detail(request, h_pk, pk):
  email = get_object_or_404(Email, pk=pk)
  hackathon = get_object_or_404(Hackathon, pk=h_pk)

  leads, non_leads = email.get_leads_and_contacts()
  contacts = combine_lead_and_contacts(leads.values_list("contact__pk", flat=True), non_leads.values_list("pk", flat=True))
  
  company_ids = set(leads.values_list("contact__company__pk", flat=True)).union(set(non_leads.values_list("company__pk", flat=True)))
  companies = [{"company": c, "sponsorship": c.sponsorships.filter(hackathon__pk=h_pk).first()} for c in Company.objects.filter(pk__in=company_ids)]

  return render(request, "email_detail_view.html", {
    "email": email,
    "hackathon": hackathon,
    "contacts": contacts,
    "companies": companies
  })

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
def compose_from_contacts(request, h_pk):
  hackathon = get_object_or_404(Hackathon, pk=h_pk)
  if request.method == "POST":
    form = ComposeFromContactsForm(request.POST)
    if form.is_valid():
      email = form.save(commit=False)
      email.hackathon = hackathon
      email.status = 'draft'
      email.save()
      email.to_contacts.set(form.cleaned_data["to_contacts"])
      email.save()
      messages.success(request, f"Created email with subject: {email.subject}")
      return redirect("emails:view", h_pk=h_pk, pk=email.pk)
  else:
    form = ComposeFromContactsForm()
  return render(request, "email_compose_from_contacts.html", {"form" : form})

@login_required
def compose_from_company(request, h_pk):
  hackathon = get_object_or_404(Hackathon, pk=h_pk)
  if request.method == "POST":
    form = ComposeFromCompanyForm(request.POST)
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
    form = ComposeFromCompanyForm()
  return render(request, "email_compose_from_company.html", {"form": form})

@login_required
def compose_from_industry(request, h_pk):
  hackathon = get_object_or_404(Hackathon, pk=h_pk)
  if request.method == "POST":
    form = ComposeFromIndustryForm(request.POST)
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
    form = ComposeFromIndustryForm()
  return render(request, "email_compose_from_industry.html", {"form": form})
