from django.shortcuts import render, redirect, get_object_or_404
from .models import Company
from .forms import CompanyForm


def new(request):
    return render(request, "new.html.j2")


def companies(request):
    companies = Company.objects.all()
    return render(request, "companies.html.j2", context={"companies": companies})


def company_new(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        print(form)
        if form.is_valid():
            company = form.save(commit=False)
            company.industries.set(form.cleaned_data["industries"])
            company.save()
            return redirect("companies:index")
    else:
        form = CompanyForm()
    return render(request, "company_new.html.j2", {"form": form})


def company_edit(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == "POST":
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            company = form.save(commit=False)
            company.industries.set(form.cleaned_data["industries"])
            company.save()
            return redirect("companies:index")
    else:
        form = CompanyForm(instance=company)
    return render(request, "company_edit.html.j2", {"form": form})
