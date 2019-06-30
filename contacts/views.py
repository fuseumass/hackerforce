from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Contact, Company
from .forms import ContactForm

@login_required
def contacts(request):
    contacts = Contact.objects.all()
    return render(request, "contacts.html", {"contacts": contacts})

@login_required
def contact_new(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
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
            return redirect("contacts:index")
    else:
        form = ContactForm(instance=contact)
    return render(request, "contact_edit.html", {"form": form})
