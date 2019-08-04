from django import forms
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from ..models import Hackathon, Sponsorship, Lead
from companies.models import Company
from contacts.models import Contact
from contacts.forms import ContactForm
from emails.models import Email
from ..forms import HackathonForm, LeadForm, SponsorshipMarkContactedForm, LeadMarkContactedForm

@login_required
def leads_show(request, h_pk):
    hackathon = get_object_or_404(Hackathon, pk=h_pk)

    def state_filter(states):
        return Lead.objects.filter(sponsorship__hackathon=hackathon, status__in=states)

    def paginator_wrapper(name, obj):
        paginator = Paginator(obj, 25)
        return paginator.get_page(request.GET.get(f"{name}_page"))
    
    def order_by_wrapper(name, obj, strip=None):
        order_by = request.GET.get(f"{name}_order_by") or "contact__last_name,contact__first_name"
        if strip and order_by:
            order_by = order_by.replace(strip, '')
        if order_by:
            obj = obj.order_by(*order_by.split(','))
        return obj
    
    def get_q(name):
        return request.GET["q"] if request.GET.get("q") else request.GET.get(f"{name}_q")
    
    def lead_wrapper(name, states):
        obj = state_filter(states)
        q = get_q(name)
        if q:
            obj = obj.filter(Q(contact__first_name__icontains=q) | Q(contact__last_name__icontains=q) | Q(contact__company__name__icontains=q) | Q(contact__company__industries__name__iexact=q))
        obj = obj.select_related()
        return paginator_wrapper(name, order_by_wrapper(name, obj.distinct()))
    
    def contact_wrapper(name):
        contacts_for_hackathon = Contact.objects.filter(leads__sponsorship__hackathon__pk=h_pk).values_list("pk", flat=True)
        obj = Contact.objects.exclude(pk__in=contacts_for_hackathon)
        q = get_q(name)
        if q:
            obj = obj.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(company__name__icontains=q))
        obj = obj.select_related()
        return paginator_wrapper(name, fake_leads(order_by_wrapper(name, obj.distinct(), 'contact__')))

    def fake_leads(contacts):
        return [Lead(pk=0, contact=c, sponsorship=Sponsorship(pk=0, company=c.company)) for c in contacts]

    responded = lead_wrapper("responded", [Lead.RESPONDED])
    contacted = lead_wrapper("contacted", [Lead.CONTACTED])
    uncontacted = contact_wrapper("uncontacted")
    dead = lead_wrapper("dead", [Lead.GHOSTED])

    return render(request, "leads_show.html", {
        "responded": responded,
        "contacted": contacted,
        "uncontacted": uncontacted,
        "dead": dead,
    })

@login_required
def lead_new(request, h_pk):
    if request.method == "POST":
        form = LeadForm(request.hackathon, None, request.POST)
        if form.is_valid():
            lead = form.save(commit=True)
            lead.save()
            return redirect("hackathons:leads:view", h_pk=h_pk, pk=lead.contact.pk)
    else:
        contact_pk = request.GET.get("contact")
        contact = get_object_or_404(Contact, pk=contact_pk) if contact_pk else None
        sponsorship = None
        company = None
        if contact:
            sponsorship = Sponsorship.objects.filter(hackathon__pk=h_pk, company__pk=contact.company.pk)
            sponsorship = sponsorship[0] if sponsorship else None
            company = get_object_or_404(Company, pk=contact.company.pk)
            if not sponsorship:
                messages.info(request, f"Before you can create a lead for {contact}, you need to begin tracking {company}. Press save below and then navigate back to the contact page.")
                return redirect(reverse("hackathons:sponsorships:new", args=(h_pk,)) + "?company=" + str(company.pk) + "&next=" + reverse("hackathons:leads:new", args=(h_pk,)) + "?company=" + str(company.pk))
        
        initial = {
            "contact": contact if contact_pk else None,
            "sponsorship": sponsorship,
        }
        form = LeadForm(request.hackathon, company, initial=initial)
    return render(request, "lead_new.html", {"form": form})

@login_required
def lead_mark_contacted(request, h_pk, c_pk):
    contact = get_object_or_404(Contact, pk=c_pk)
    company = get_object_or_404(Company, pk=contact.company.pk)
    sponsorship = Sponsorship.objects.filter(hackathon__pk=h_pk, company__pk=contact.company.pk)
    sponsorship = sponsorship[0] if sponsorship else None
    if Lead.objects.filter(sponsorship=sponsorship, contact=contact):
        messages.info(request, f"{contact} has already been contacted for {sponsorship.hackathon}")
        return redirect("hackathons:leads:edit", h_pk=h_pk, pk=contact.pk)
    
    sp_initial = {
        "hackathon": get_object_or_404(Hackathon, pk=h_pk),
        "company": company,
    }
    if request.method == "POST":
        if sponsorship:
            sp_form = SponsorshipMarkContactedForm(request.POST, instance=sponsorship, prefix="sponsorship")
        else:
            sp_form = SponsorshipMarkContactedForm(request.POST, prefix="sponsorship")
        
        l_form = LeadMarkContactedForm(request.hackathon, company, request.POST.copy(), prefix="lead")
        if sp_form.is_valid():
            sp = sp_form.save(commit=True)
            l_form.data['lead-sponsorship'] = str(sp.pk)
            print('l_form', l_form.data)
            if l_form.is_valid():
                l = l_form.save(commit=True)
                l.save()
                sp.save()
                messages.success(request, f"Marked {contact} as contacted")
                if request.GET.get("next"):
                    return redirect(request.GET.get("next"))
                return redirect("hackathons:leads:view", h_pk=h_pk, pk=contact.pk)
    else:
        if sponsorship:
            sp_form = SponsorshipMarkContactedForm(instance=sponsorship, prefix="sponsorship")
        else:
            sp_form = SponsorshipMarkContactedForm(initial=sp_initial, prefix="sponsorship")

        l_form = LeadMarkContactedForm(request.hackathon, company, initial={
            "contact": contact,
            "sponsorship": sponsorship,
        }, prefix="lead")

    return render(request, "lead_mark_contacted.html", {
        "sp_form": sp_form,
        "l_form": l_form,
        "sponsorship": sponsorship,
        "contact": contact,
    })

@login_required
def lead_edit(request, h_pk, pk):
    lead = Lead.objects.filter(sponsorship__hackathon__pk=h_pk, contact__pk=pk)
    lead = lead[0] if lead else None
    if not lead:
        return redirect(reverse("contacts:edit", args=(pk,))+"?next="+reverse("hackathons:leads:view", args=(h_pk,pk,)))
    if request.method == "POST":
        lead_form = LeadForm(request.hackathon, lead.sponsorship.company, request.POST, instance=lead, prefix="lead")
        if lead_form.is_valid():
            lead = lead_form.save(commit=True)
            lead.save()
            ok = True
        else:
            ok = False
        contact_form = ContactForm(request.POST, instance=lead.contact, prefix="contact")
        if contact_form.is_valid():
            contact = contact_form.save(commit=True)
            contact.save()
            ok = ok and True
        else:
            ok = False
        if ok:
            messages.success(request, f"Updated {lead.contact}")
            if request.GET.get("next"):
                return redirect(request.GET.get("next"))
            return redirect("hackathons:leads:view", h_pk=h_pk, pk=lead.contact.pk)
    else:
        lead_form = LeadForm(request.hackathon, lead.sponsorship.company, instance=lead, prefix="lead")
        contact_form = ContactForm(instance=lead.contact, prefix="contact")
    lead_form.fields['sponsorship'].widget = forms.HiddenInput()
    lead_form.fields['contact'].widget = forms.HiddenInput()
    return render(request, "lead_edit.html", {"lead_form": lead_form, "contact_form": contact_form})

@login_required
def lead_detail(request, h_pk, pk):
    return render(request, "lead_detail.html", lead_detail_context(request, h_pk, pk))

def lead_detail_context(request, h_pk, pk):
    contact = get_object_or_404(Contact, pk=pk)

    lead = Lead.objects.filter(sponsorship__hackathon__pk=h_pk, contact__pk=pk)
    lead = lead[0] if lead else None

    sponsorship = Sponsorship.objects.filter(hackathon__pk=h_pk, company__pk=contact.company.pk)
    sponsorship = sponsorship[0] if sponsorship else None

    lead_contacts = sponsorship.leads.all().values_list('contact__id', flat=True) if sponsorship else []
    non_lead_contacts = set(contact.company.contacts.all().values_list('id', flat=True)) - set(lead_contacts)

    contacts = [{"lead": lead, "contact": lead.contact} for lead in Lead.objects.filter(contact__id__in=lead_contacts)]
    contacts += [{"contact": contact} for contact in Contact.objects.filter(id__in=non_lead_contacts)]

    emails = Email.objects.filter(sent_contacts=contact)

    return {
        "lead": lead,
        "contact": contact,
        "sponsorship": sponsorship,
        "contacts": contacts,
        "emails": emails,
    }



@login_required
def lead_delete(request, h_pk, pk):
    lead = get_object_or_404(Lead, sponsorship__hackathon__pk=h_pk, contact__pk=pk)
    if request.method == "POST" and request.POST.get("delete") == "yes":
        lead.delete()
        messages.success(request, f"Marked {lead} as uncontacted")
        if request.GET.get("next"):
            return redirect(request.GET.get("next"))
        return redirect("hackathons:leads:view", h_pk, lead.contact.pk)
    return render(request, "lead_delete.html", lead_detail_context(request, h_pk, pk))
