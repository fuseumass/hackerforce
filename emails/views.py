from pprint import pformat
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from contacts.models import Contact
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
    email = get_object_or_404(Email, hackathon__pk=h_pk, pk=pk)
    hackathon = get_object_or_404(Hackathon, pk=h_pk)

    leads, non_leads = email.get_leads_and_contacts()
    contacts = combine_lead_and_contacts(leads.values_list(
        "contact__pk", flat=True), non_leads.values_list("pk", flat=True))

    company_ids = set(leads.values_list("contact__company__pk", flat=True)).union(
        set(non_leads.values_list("company__pk", flat=True)))
    companies = [{"company": c, "sponsorship": c.sponsorships.filter(
        hackathon__pk=h_pk).first()} for c in Company.objects.filter(pk__in=company_ids)]

    uses_context = ("{" + "{") in email.body

    return render(request, "email_detail_view.html", {
        "email": email,
        "hackathon": hackathon,
        "contacts": contacts,
        "companies": companies,
        "uses_context": uses_context,
    })

@login_required
def email_edit(request, h_pk, pk):
    email = get_object_or_404(Email, hackathon__pk=h_pk, pk=pk)
    if email.email_type == Email.FROM_INDUSTRY:
        return redirect(reverse("emails:compose_from_industry", args=(h_pk,))+f"?pk={email.pk}")


@login_required
def render_message(request, h_pk, pk):
    email = get_object_or_404(Email, hackathon__pk=h_pk, pk=pk)
    contact_pk = request.GET.get("contact_pk")
    contact = get_object_or_404(Contact, pk=contact_pk) if contact_pk else None

    message = email.render_body(contact)
    cvars = {k: vars(v) if v else None for k,
             v in email.render_body_context(contact).items()}
    context = pformat(cvars, indent=2)

    return render(request, "email_render_message.html", {
        "email": email,
        "message": message,
        "contact": contact,
        "context": context,
    })


@login_required
def send_message(request, h_pk, pk):
    email = get_object_or_404(Email, hackathon__pk=h_pk, pk=pk)

    leads, non_leads = email.get_leads_and_contacts()
    contacts = combine_lead_and_contacts(leads.values_list(
        "contact__pk", flat=True), non_leads.values_list("pk", flat=True))
    
    for c in contacts:
        print("contact", c)
        message = email.render_body(c.contact)
        print("message:", message)

    return render(request, "email_send_message.html", {
        "email": email,
        "contacts": contacts,
    })


@login_required
def drafts(request, h_pk):
    hackathon = get_object_or_404(Hackathon, pk=h_pk)
    emails = Email.objects.filter(hackathon=hackathon)

    order_by = request.GET.get("order_by") or "internal_title"
    if order_by:
        emails = emails.order_by(*order_by.split(","))

    paginator = Paginator(emails, 25)
    page = request.GET.get("page")
    emails = paginator.get_page(page)
    return render(request, "email_drafts.html", {"emails": emails})


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
            messages.success(
                request, f"Created email with subject: {email.subject}")
            return redirect("emails:view", h_pk=h_pk, pk=email.pk)
    else:
        form = ComposeFromContactsForm()
    return render(request, "email_compose_from_contacts.html", {"form": form})


@login_required
def compose_from_company(request, h_pk):
    hackathon = get_object_or_404(Hackathon, pk=h_pk)
    existing_pk = request.GET.get("pk")
    existing = get_object_or_404(Email, pk=existing_pk) if existing_pk else None
    if request.method == "POST":
        if existing_pk:
            form = ComposeFromCompanyForm(request.POST, instance=existing)
        else:
            form = ComposeFromCompanyForm(request.POST)
        if form.is_valid():
            email = form.save(commit=False)
            email.hackathon = hackathon
            if not existing_pk:
                email.status = 'draft'
            email.save()
            email.to_companies.set(form.cleaned_data["to_companies"])
            email.save()
            if existing_pk:
                messages.success(
                request, f"Updated email: {email.internal_title}")
            else:
                messages.success(
                    request, f"Created email: {email.internal_title}")
            return redirect("emails:view", h_pk=h_pk, pk=email.pk)
    elif existing_pk:
        form = ComposeFromCompanyForm(instance=existing)
    else:
        form = ComposeFromCompanyForm()
    return render(request, "email_compose_from_company.html", {"form": form})


@login_required
def compose_from_industry(request, h_pk):
    hackathon = get_object_or_404(Hackathon, pk=h_pk)
    existing_pk = request.GET.get("pk")
    existing = get_object_or_404(Email, pk=existing_pk) if existing_pk else None
    if request.method == "POST":
        if existing_pk:
            form = ComposeFromIndustryForm(request.POST, instance=existing)
        else:
            form = ComposeFromIndustryForm(request.POST)
        if form.is_valid():
            email = form.save(commit=False)
            email.hackathon = hackathon
            if not existing_pk:
                email.status = 'draft'
            email.save()
            email.to_industries.set(form.cleaned_data["to_industries"])
            email.save()
            if existing_pk:
                messages.success(
                request, f"Updated email: {email.internal_title}")
            else:
                messages.success(
                    request, f"Created email: {email.internal_title}")
            return redirect("emails:view", h_pk=h_pk, pk=email.pk)
    elif existing_pk:
        form = ComposeFromIndustryForm(instance=existing)
    else:
        form = ComposeFromIndustryForm()

    return render(request, "email_compose_from_industry.html", {"form": form, "existing": existing})
