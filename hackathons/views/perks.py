from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Perk
from ..forms import PerkForm

from hackathons.models import Hackathon

@login_required
def perk_new(request):
    hackathon_id = request.GET.get("hackathon")
    if request.method == "POST":
        form = PerkForm(request.POST)
        if form.is_valid():
            perk = form.save(commit=False)
            perk.save()
            messages.success(request, f"Added perk {perk}")
            if request.GET.get("next"):
                return redirect(request.GET.get("next"))
            return redirect("hackathons:index")
    elif hackathon_id:
        form = PerkForm(initial={"hackathon": get_object_or_404(Hackathon, pk=hackathon_id)})
    else:
        form = PerkForm()
    return render(request, "perk_new.html", {"form": form})

@login_required
def perk_edit(request, pk):
    perk = get_object_or_404(Perk, pk=pk)
    if request.method == "POST":
        form = PerkForm(request.POST, instance=perk)
        if form.is_valid():
            perk = form.save(commit=False)
            perk.save()
            messages.success(request, f"Edited perk {perk}")
            if request.GET.get("next"):
                return redirect(request.GET.get("next"))
            return redirect("hackathons:index")
    else:
        form = PerkForm(instance=perk)
    return render(request, "perk_edit.html", {"form": form})

@login_required
def perk_detail(request, h_pk, pk):
    perk = get_object_or_404(Perk, pk=pk)
    perk_url = reverse("hackathons:perks:edit", args=(pk,)) + "?next=" + reverse("dashboard:view", args=(h_pk,))
    messages.info(request, f"Showing sponsorships with perk {perk.name}. <a href='{perk_url}'>Edit this perk</a>", extra_tags="info safe")
    return redirect(reverse("hackathons:sponsorships:show", args=(h_pk,)) + f"?q={perk.name}")