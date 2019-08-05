from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Company, Industry
from contacts.models import Contact
from hackathons.models import Sponsorship, Lead
from .forms import CompanyForm, IndustryForm

# @login_required
# def new(request):
#     return render(request, "new.html")

@login_required
def companies(request):
    q = request.GET.get("q")
    if q:
        companies = Company.objects.filter(Q(name__icontains=q) | Q(industries__name__iexact=q))
    else:
        companies = Company.objects.all()
    
    order_by = request.GET.get("order_by")
    if order_by:
        companies = companies.order_by(*order_by.split(","))

    paginator = Paginator(companies.distinct(), 25)
    page = request.GET.get("page")
    companies = paginator.get_page(page)
    return render(request, "companies.html", context={"companies": companies})

@login_required
def company_new(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save(commit=True)
            company.industries.set(form.cleaned_data["industries"])
            company.save()
            messages.success(request, f"Added {company}")
            if request.GET.get("next"):
                return redirect(request.GET.get("next"))
            return redirect("companies:index")
    else:
        form = CompanyForm()
    return render(request, "company_new.html", {"form": form})

@login_required
def company_edit(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == "POST":
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            company = form.save(commit=True)
            company.industries.set(form.cleaned_data["industries"])
            company.save()
            messages.success(request, f"Updated {company.name}")
            if request.GET.get("next"):
                return redirect(request.GET.get("next"))
            return redirect("companies:view", pk=company.pk)
    else:
        form = CompanyForm(instance=company)
    return render(request, "company_edit.html", {"form": form, "company": company})

@login_required
def company_delete(request, pk):
    company = get_object_or_404(Company, pk=pk)
    contacts = Contact.objects.filter(company=company)
    sponsorships = Sponsorship.objects.filter(company=company)
    leads = Lead.objects.filter(sponsorship__in=sponsorships)
    if request.method == "POST" and request.POST.get("delete") == "yes":
        company.delete()
        messages.success(request, f"Deleted {company}")
        if request.GET.get("next"):
            return redirect(request.GET.get("next"))
        return redirect("companies:index")
    return render(request, "company_delete.html", {
        "company": company,
        "contacts": contacts,
        "sponsorships": sponsorships,
        "leads": leads,
    })

@login_required
def company_detail(request, pk):
    company = get_object_or_404(Company, pk=pk)
    contacts = Contact.objects.filter(company=company)
    sponsorships = Sponsorship.objects.filter(company=company)
    return render(request, "company_detail.html", context={
        "company": company,
        "contacts": contacts,
        "sponsorships": sponsorships,
    })

@login_required
def industries(request):
    industries = Industry.objects.all()
    return render(request, "industries.html", {
        "industries": industries,
    })

@login_required
def industry_new(request):
    if request.method == "POST":
        form = IndustryForm(request.POST)
        if form.is_valid():
            industry = form.save(commit=True)
            industry.save()
            messages.success(request, f"Added {industry}")
            if request.GET.get("next"):
                return redirect(request.GET.get("next"))
            return redirect("companies:industries:index")
    else:
        form = IndustryForm()
    return render(request, "industry_new.html", {"form": form})

@login_required
def industry_edit(request, pk):
    industry = get_object_or_404(Industry, pk=pk)
    if request.method == "POST":
        form = IndustryForm(request.POST, instance=industry)
        if form.is_valid():
            industry = form.save(commit=True)
            industry.save()
            messages.success(request, f"Updated {industry}")
            if request.GET.get("next"):
                return redirect(request.GET.get("next"))
            return redirect("companies:industries:index")
    else:
        form = IndustryForm(instance=industry)
    return render(request, "industry_edit.html", {"form": form, "industry": industry})

@login_required
def industry_delete(request, pk):
    industry = get_object_or_404(Industry, pk=pk)
    if request.method == "POST" and request.POST.get("delete") == "yes":
        industry.delete()
        messages.success(request, f"Deleted {industry}")
        if request.GET.get("next"):
            return redirect(request.GET.get("next"))
        return redirect("companies:industries:index")
    return render(request, "industry_delete.html", {
        "industry": industry,
    })
