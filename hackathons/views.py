from django.shortcuts import render, redirect, get_object_or_404

from .models import Tier, Perk, Hackathon, Sponsorship
from .forms import TierForm, PerkForm, HackathonForm, SponsorshipForm


def hackathons(request):
    hackathons = Hackathon.objects.all()
    return render(request, "hackathons.html.j2", {"hackathons": hackathons})


def hackathon_show(request, pk):
    hackathon = get_object_or_404(Hackathon, pk=pk)
    return render(request, "hackathon_show.html.j2", {"hackathon": hackathon})


def sponsorships_show(request, pk):
    hackathon = get_object_or_404(Hackathon, pk=pk)
    return render(request, "sponsorships_show.html.j2", {"hackathon": hackathon})


def hackathon_new(request):
    if request.method == "POST":
        form = HackathonForm(request.POST)
        if form.is_valid():
            hackathon = form.save(commit=False)
            hackathon.save()
            return redirect("hackathons:index")
    else:
        form = HackathonForm()
    return render(request, "hackathon_new.html.j2", {"form": form})


def hackathon_edit(request, pk):
    hackathon = get_object_or_404(Hackathon, pk=pk)
    if request.method == "POST":
        form = HackathonForm(request.POST, instance=hackathon)
        if form.is_valid():
            hackathon = form.save(commit=False)
            hackathon.save()
            return redirect("hackathons:index")
    else:
        form = HackathonForm(instance=hackathon)
    return render(request, "hackathon_edit.html.j2", {"form": form})


def tier_new(request):
    if request.method == "POST":
        form = TierForm(request.POST)
        if form.is_valid():
            tier = form.save(commit=False)
            tier.save()
            return redirect("hackathons:index")
    else:
        form = TierForm()
    return render(request, "tier_new.html.j2", {"form": form})


def tier_edit(request, pk):
    tier = get_object_or_404(Tier, pk=pk)
    if request.method == "POST":
        form = TierForm(request.POST, instance=tier)
        if form.is_valid():
            tier = form.save(commit=False)
            tier.save()
            return redirect("hackathons:index")
    else:
        form = TierForm(instance=tier)
    return render(request, "tier_edit.html.j2", {"form": form})


def perk_new(request):
    if request.method == "POST":
        form = PerkForm(request.POST)
        if form.is_valid():
            perk = form.save(commit=False)
            return redirect("hackathons:index")
    else:
        form = PerkForm()
    return render(request, "perk_new.html.j2", {"form": form})


def perk_edit(request, pk):
    perk = get_object_or_404(Perk, pk=pk)
    if request.method == "POST":
        form = PerkForm(request.POST, instance=perk)
        if form.is_valid():
            perk = form.save(commit=False)
            perk.save()
            return redirect("hackathons:index")
    else:
        form = PerkForm(instance=perk)
    return render(request, "perk_edit.html.j2", {"form": form})


def sponsorship_new(request):
    if request.method == "POST":
        form = SponsorshipForm(request.POST)
        if form.is_valid():
            sponsorship = form.save(commit=True)
            sponsorship.perks.set(form.cleaned_data["perks"])
            sponsorship.tiers.set(form.cleaned_data["tiers"])
            sponsorship.save()
            return redirect("hackathons:index")
    else:
        form = SponsorshipForm()
    return render(request, "sponsorship_new.html.j2", {"form": form})


def sponsorship_edit(request, pk):
    sponsorship = get_object_or_404(Sponsorship, pk=pk)
    if request.method == "POST":
        form = SponsorshipForm(request.POST, instance=sponsorship)
        if form.is_valid():
            sponsorship = form.save(commit=True)
            sponsorship.perks.set(form.cleaned_data["perks"])
            sponsorship.tiers.set(form.cleaned_data["tiers"])
            sponsorship.save()
            return redirect("hackathons:index")
    else:
        form = SponsorshipForm(instance=sponsorship)
    return render(request, "sponsorship_edit.html.j2", {"form": form})
