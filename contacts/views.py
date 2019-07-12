from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from hackathons.models import Hackathon, Lead, Sponsorship
from .models import Contact, Company
from .forms import ContactForm

@login_required
def contacts(request):
    q = request.GET.get("q")
    if q:
        contacts = Contact.objects.filter(Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(company__name__icontains=q))
    else:
        contacts = Contact.objects.all()
        
    order_by = request.GET.get("order_by") or "last_name,first_name"
    if order_by:
        contacts = contacts.order_by(*order_by.split(","))

    paginator = Paginator(contacts, 25)
    page = request.GET.get("page")
    contacts = paginator.get_page(page)
    return render(request, "contacts.html", {"contacts": contacts})

@login_required
def contact_new(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
            messages.success(request, f"Added {contact}")
            if request.GET.get("next"):
                return redirect(request.GET.get("next"))
            return redirect("contacts:index")
    elif request.GET.get("company_id") is not None:
        company = get_object_or_404(Company, pk=request.GET.get("company_id"))
        form = ContactForm(initial={"company": company})
    else:
        form = ContactForm()
    return render(request, "contact_new.html", {"form": form})

@login_required
def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
            messages.success(request, f"Updated {contact}")
            if request.GET.get("next"):
                return redirect(request.GET.get("next"))
            return redirect("contacts:view", pk=contact.pk)
    else:
        form = ContactForm(instance=contact)
    return render(request, "contact_edit.html", {"form": form, "contact": contact})

@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    leads = Lead.objects.filter(contact=contact)
    sponsorships = Sponsorship.objects.filter(company=contact.company)
    if request.method == "POST" and request.POST.get("delete") == "yes":
        contact.delete()
        messages.success(request, f"Deleted {contact}")
        return redirect("contacts:index")
    return render(request, "contact_delete.html", {"contact": contact, "leads": leads, "sponsorships": sponsorships})

@login_required
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    leads = Lead.objects.filter(contact=contact)
    sponsorships = Sponsorship.objects.filter(company=contact.company)
    return render(request, "contact_detail.html", {"contact": contact, "leads": leads, "sponsorships": sponsorships})
