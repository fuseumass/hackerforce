from django.shortcuts import render, redirect, get_object_or_404

from .models import Contact
from .forms import ContactForm


def contacts(request):
    contacts = Contact.objects.all()
    return render(request, "contacts.html.j2", {"contacts": contacts})


def contact_new(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
            return redirect("contacts:index")
    else:
        form = ContactForm()
    return render(request, "contact_new.html.j2", {"form": form})


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
    return render(request, "contact_edit.html.j2", {"form": form})
