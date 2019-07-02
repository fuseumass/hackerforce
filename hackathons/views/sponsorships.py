from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Tier, Perk, Hackathon, Sponsorship
from ..forms import TierForm, PerkForm, HackathonForm, SponsorshipForm

def sponsorships_show(request, h_pk):
    hackathon = get_object_or_404(Hackathon, pk=h_pk)
    return render(request, "sponsorships_show.html", {"hackathon": hackathon})

def sponsorship_new(request):
    if request.method == "POST":
        form = SponsorshipForm(request.POST)
        if form.is_valid():
            sponsorship = form.save(commit=True)
            sponsorship.perks.set(form.cleaned_data["perks"])
            # sponsorship.tiers.set(form.cleaned_data["tiers"])
            sponsorship.save()
            return redirect("hackathons:sponsorships_show", pk=sponsorship.hackathon.pk)
    else:
        form = SponsorshipForm()
    return render(request, "sponsorship_new.html", {"form": form})

def sponsorship_edit(request, h_pk, pk):
    sponsorship = get_object_or_404(Sponsorship, hackathon__pk=h_pk, pk=pk)
    if request.method == "POST":
        form = SponsorshipForm(request.POST, instance=sponsorship)
        if form.is_valid():
            sponsorship = form.save(commit=True)
            sponsorship.perks.set(form.cleaned_data["perks"])
            # sponsorship.tiers.set(form.cleaned_data["tiers"])
            sponsorship.save()
            return redirect("hackathons:sponsorships_show", pk=sponsorship.hackathon.pk)
    else:
        form = SponsorshipForm(instance=sponsorship)
    return render(request, "sponsorship_edit.html", {"form": form})

def sponsorship_detail(request, h_pk, pk):
    sponsorship = get_object_or_404(Sponsorship, hackathon__pk=h_pk, pk=pk)
    return render(request, "sponsorship_detail.html", {"sponsorship": sponsorship})
