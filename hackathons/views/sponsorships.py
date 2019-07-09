from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from ..models import Hackathon, Sponsorship, Lead
from companies.models import Company
from contacts.models import Contact
from ..forms import HackathonForm, SponsorshipForm

@login_required
def sponsorships_show(request, h_pk):
    hackathon = get_object_or_404(Hackathon, pk=h_pk)

    def state_filter(states):
        return Sponsorship.objects.filter(hackathon=hackathon, status__in=states)

    def paginator_wrapper(name, obj):
        order_by = request.GET.get(f"{name}_order_by")
        if order_by:
            obj = obj.order_by(order_by)
        paginator = Paginator(obj, 25)
        return paginator.get_page(request.GET.get(f"{name}_page"))
    
    def get_q(name):
        return request.GET["q"] if request.GET.get("q") else request.GET.get(f"{name}_q")
    
    def sponsorship_wrapper(name, states):
        obj = state_filter(states)
        q = get_q(name)
        if q:
            obj = obj.filter(Q(company__name__icontains=q) | Q(company__industries__name__iexact=q))
        return paginator_wrapper(name, obj.distinct())
    
    def company_wrapper(name):
        companies_for_hackathon = Company.objects.filter(sponsorships__hackathon__pk=h_pk).values_list("pk", flat=True)
        obj = Company.objects.exclude(pk__in=companies_for_hackathon)
        q = get_q(name)
        if q:
            obj = obj.filter(Q(name__icontains=q) | Q(industries__name__iexact=q))
        return paginator_wrapper(name, fake_sponsorship(obj.distinct()))

    def fake_sponsorship(company):
        return [Sponsorship(pk=0, company=c, tier=None, contribution=0) for c in company]
    
    confirmed = sponsorship_wrapper("confirmed", [Sponsorship.CONFIRMED, Sponsorship.PAID])
    in_progress = sponsorship_wrapper("in_progress", [Sponsorship.CONTACTED, Sponsorship.RESPONDED])
    dead = sponsorship_wrapper("dead", [Sponsorship.GHOSTED, Sponsorship.DENIED])
    uncontacted = company_wrapper("companies")

    return render(request, "sponsorships_show.html", {
        "confirmed": confirmed,
        "in_progress": in_progress,
        "dead": dead,
        "uncontacted": uncontacted,
    })

@login_required
def sponsorship_new(request, h_pk):
    if request.method == "POST":
        form = SponsorshipForm(request.POST)
        if form.is_valid():
            sponsorship = form.save(commit=True)
            sponsorship.perks.set(form.cleaned_data["perks"])
            # sponsorship.tiers.set(form.cleaned_data["tiers"])
            sponsorship.save()
            return redirect("hackathons:sponsorships:view", h_pk=h_pk, pk=sponsorship.company.pk)
    else:
        company_pk = request.GET.get("company")
        initial = {
            "hackathon": get_object_or_404(Hackathon, pk=h_pk),
            "company": get_object_or_404(Company, pk=company_pk) if company_pk else None,
        }
        form = SponsorshipForm(initial=initial)
    return render(request, "sponsorship_new.html", {"form": form})

@login_required
def sponsorship_edit(request, h_pk, pk):
    sponsorship = get_object_or_404(Sponsorship, hackathon__pk=h_pk, company__pk=pk)
    if request.method == "POST":
        form = SponsorshipForm(request.POST, instance=sponsorship)
        if form.is_valid():
            sponsorship = form.save(commit=True)
            sponsorship.perks.set(form.cleaned_data["perks"])
            # sponsorship.tiers.set(form.cleaned_data["tiers"])
            sponsorship.save()
            return redirect("hackathons:sponsorships:view", h_pk=h_pk, pk=sponsorship.company.pk)
    else:
        form = SponsorshipForm(instance=sponsorship)
    return render(request, "sponsorship_edit.html", {"form": form})

@login_required
def sponsorship_detail(request, h_pk, pk):
    company = get_object_or_404(Company, pk=pk)

    sponsorship = Sponsorship.objects.filter(hackathon__pk=h_pk, company__pk=pk)
    sponsorship = sponsorship[0] if sponsorship else None

    lead_contacts = sponsorship.leads.all().values_list('contact__id', flat=True) if sponsorship else []
    non_lead_contacts = set(company.contacts.all().values_list('id', flat=True)) - set(lead_contacts)

    contacts = combine_lead_and_contacts(lead_contacts, non_lead_contacts)

    return render(request, "sponsorship_detail.html", {
        "sponsorship": sponsorship,
        "company": company,
        "contacts": contacts,
        "no_contacted_employees": len(lead_contacts) == 0 if sponsorship else False
    })

def combine_lead_and_contacts(lead_contact_ids, non_lead_contact_ids):
    contacts = [{"lead": lead, "contact": lead.contact} for lead in Lead.objects.filter(contact__id__in=lead_contact_ids)]
    contacts += [{"contact": contact} for contact in Contact.objects.filter(id__in=non_lead_contact_ids)]

    return contacts
