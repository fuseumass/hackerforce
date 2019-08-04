from pprint import pformat
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from contacts.models import Contact
from companies.models import Company
from emails.sending import send_email_now
from hackathons.models import Hackathon
from hackathons.views.sponsorships import combine_lead_and_contacts

from .models import Email
from .forms import ComposeFromContactsForm, ComposeFromCompanyForm, ComposeFromIndustryForm, EmailChangeTypeForm

# Create your views here.
@login_required
def emails(request, h_pk):
    hackathon = get_object_or_404(Hackathon, pk=h_pk)
    return render(request, "email_compose.html", {})


@login_required
def email_detail(request, h_pk, pk):
    return render(request, "email_detail.html", email_detail_context(request, h_pk, pk))

def email_detail_context(request, h_pk, pk):
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

    return {
        "email": email,
        "hackathon": hackathon,
        "contacts": contacts,
        "companies": companies,
        "uses_context": uses_context,
    }

@login_required
def email_edit(request, h_pk, pk):
    email = get_object_or_404(Email, hackathon__pk=h_pk, pk=pk)
    return redirect(compose_route_for(email.email_type, h_pk, pk))

def compose_route_for(email_type, h_pk, email_pk):
    if email_type == Email.FROM_CONTACTS:
        route = "emails:compose_from_contacts"
    elif email_type == Email.FROM_COMPANY:
        route = "emails:compose_from_company"
    elif email_type == Email.FROM_INDUSTRY:
        route = "emails:compose_from_industry"
    return reverse(route, args=(h_pk,))+f"?pk={email_pk}"

@login_required
def email_change_type(request, h_pk, pk):
    email = get_object_or_404(Email, hackathon__pk=h_pk, pk=pk)
    
    if request.method == "POST":
        form = EmailChangeTypeForm(request.POST)
        if form.is_valid():
            email.clear_current_type()
            email.save()
            
            new_type = form.cleaned_data["new_type"]
            messages.success(request, f"Changed type for {email} to {new_type}")
            return redirect(compose_route_for(new_type, h_pk, pk))

    form = EmailChangeTypeForm()
    return render(request, "email_change_type.html", {"form": form, "email": email})

@login_required
def email_delete(request, h_pk, pk):
    email = get_object_or_404(Email, hackathon__pk=h_pk, pk=pk)

    if request.method == "POST" and request.POST.get("delete") == "yes":
        email.delete()
        messages.success(request, f"Deleted {email}")
        return redirect("emails:show", h_pk=h_pk)
    return render(request, "email_delete.html", email_detail_context(request, h_pk, pk))


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

    if request.method == "POST" and request.POST.get("send_now") == "yes":
        
        
        for c in contacts:
            contact = c['contact']
            message = email.render_body(contact)
            print(f"SENDING: {email.subject} TO: {contact} ({contact.email})")
            print(send_email_now(email.subject, message, contact.email))

        
        num = len(contacts)

        messages.success(request, f"Sent email to {num} contacts.")
        return redirect("emails:view", h_pk=h_pk, pk=pk)

    context = email_detail_context(request, h_pk, pk)
    context["contacts_to_send"] = contacts
    context["num_recipients"] = len(contacts)
    return render(request, "email_send_message.html", context)


@login_required
def show(request, h_pk):
    hackathon = get_object_or_404(Hackathon, pk=h_pk)
    drafts = show_card(request, Email.objects.filter(hackathon=hackathon, status="draft"), "draft")
    scheduled = show_card(request, Email.objects.filter(hackathon=hackathon, status="scheduled"), "scheduled")
    sent = show_card(request, Email.objects.filter(hackathon=hackathon, status="sent"), "sent")
    
    return render(request, "email_show.html", {
        "drafts": drafts,
        "scheduled": scheduled,
        "sent": sent
    })

def show_card(request, emails, pfx):
    q = request.GET["q"] if request.GET.get("q") else request.GET.get(f"{pfx}_q")
    if q:
        emails = emails.filter(Q(internal_title__icontains=q) | Q(subject__icontains=q))

    order_by = request.GET.get(f"{pfx}_order_by") or "internal_title"
    if order_by:
        emails = emails.order_by(*order_by.split(","))
    

    paginator = Paginator(emails, 25)
    page = request.GET.get(f"{pfx}_page")
    return paginator.get_page(page)

@login_required
def sent(request, h_pk):
    return render(request, "email_sent.html")

@login_required
def compose_from_contacts(request, h_pk):
    hackathon = get_object_or_404(Hackathon, pk=h_pk)
    existing_pk = request.GET.get("pk")
    existing = get_object_or_404(Email, pk=existing_pk) if existing_pk else None
    if request.method == "POST":
        if existing_pk:
            form = ComposeFromContactsForm(request.POST, instance=existing)
        else:
            form = ComposeFromContactsForm(request.POST)
        if form.is_valid():
            email = form.save(commit=False)
            email.hackathon = hackathon
            if not existing_pk:
                email.status = 'draft'
            email.save()
            email.to_contacts.set(form.cleaned_data["to_contacts"])
            email.save()
            if existing_pk:
                messages.success(
                request, f"Updated email: {email.internal_title}")
            else:
                messages.success(
                    request, f"Created email: {email.internal_title}")
            return redirect("emails:view", h_pk=h_pk, pk=email.pk)
    elif existing_pk:
        form = ComposeFromContactsForm(instance=existing)
    else:
        form = ComposeFromContactsForm()
    return render(request, "email_compose_from_contacts.html", {"form": form, "existing": existing})


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
    return render(request, "email_compose_from_company.html", {"form": form, "existing": existing})


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
