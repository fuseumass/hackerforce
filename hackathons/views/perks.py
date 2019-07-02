from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import Tier, Perk, Hackathon, Sponsorship
from ..forms import TierForm, PerkForm, HackathonForm, SponsorshipForm

def perk_new(request):
    if request.method == "POST":
        form = PerkForm(request.POST)
        if form.is_valid():
            perk = form.save(commit=False)
            perk.save()
            return redirect("hackathons:index")
    else:
        form = PerkForm()
    return render(request, "perk_new.html", {"form": form})


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
    return render(request, "perk_edit.html", {"form": form})
