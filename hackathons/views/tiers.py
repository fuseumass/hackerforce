from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Tier, Perk, Hackathon, Sponsorship
from ..forms import TierForm, PerkForm, HackathonForm, SponsorshipForm

@login_required
def tier_new(request):
    hackathon_id = request.GET.get("hackathon")
    if request.method == "POST":
        form = TierForm(request.POST)
        if form.is_valid():
            tier = form.save(commit=False)
            tier.save()
            if request.GET.get("next"):
                return redirect(request.GET.get("next"))
            return redirect("hackathons:index")
    elif hackathon_id:
        form = TierForm(initial={"hackathon": get_object_or_404(Hackathon, pk=hackathon_id)})
    else:
        form = TierForm()
    return render(request, "tier_new.html", {"form": form})

@login_required
def tier_edit(request, pk):
    tier = get_object_or_404(Tier, pk=pk)
    if request.method == "POST":
        form = TierForm(request.POST, instance=tier)
        if form.is_valid():
            tier = form.save(commit=False)
            tier.save()
            if request.GET.get("next"):
                return redirect(request.GET.get("next"))
            return redirect("hackathons:index")
    else:
        form = TierForm(instance=tier)
    return render(request, "tier_edit.html", {"form": form})

@login_required
def tier_detail(request, h_pk, pk):
    tier = get_object_or_404(Tier, pk=pk)
    messages.info(request, f"Showing sponsorships with tier {tier.name}")
    return redirect(reverse("hackathons:sponsorships:show", args=(h_pk,)) + f"?q={tier.name}")