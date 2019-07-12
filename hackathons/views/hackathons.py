from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Hackathon
from ..forms import HackathonForm

def hackathons(request):
    hackathons = Hackathon.objects.all()
    return render(request, "hackathons.html", {"hackathons": hackathons})

def hackathon_new(request):
    if request.method == "POST":
        form = HackathonForm(request.POST)
        if form.is_valid():
            hackathon = form.save(commit=False)
            hackathon.save()
            messages.success(request, f"Created hackathon {hackathon}")
            if request.GET.get("next"):
                return redirect(request.GET.get("next"))
            return redirect("dashboard:view", pk=hackathon.pk)
    else:
        form = HackathonForm()
    return render(request, "hackathon_new.html", {"form": form})

def hackathon_edit(request, h_pk):
    hackathon = get_object_or_404(Hackathon, pk=h_pk)
    if request.method == "POST":
        form = HackathonForm(request.POST, instance=hackathon, hackathon=hackathon)
        if form.is_valid():
            hackathon = form.save(commit=False)
            hackathon.tiers.set(form.cleaned_data["tiers"])
            hackathon.perks.set(form.cleaned_data["perks"])
            hackathon.save()
            messages.success(request, f"Edited hackathon {hackathon}")
            if request.GET.get("next"):
                return redirect(request.GET.get("next"))
            return redirect("hackathons:index")
    else:
        form = HackathonForm(instance=hackathon, hackathon=hackathon)
    return render(request, "hackathon_edit.html", {"form": form})

