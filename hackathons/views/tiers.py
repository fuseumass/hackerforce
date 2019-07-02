from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Tier, Perk, Hackathon, Sponsorship
from ..forms import TierForm, PerkForm, HackathonForm, SponsorshipForm

def tier_new(request):
    if request.method == "POST":
        form = TierForm(request.POST)
        if form.is_valid():
            tier = form.save(commit=False)
            tier.save()
            return redirect("hackathons:index")
    else:
        form = TierForm()
    return render(request, "tier_new.html", {"form": form})

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
    return render(request, "tier_edit.html", {"form": form})
