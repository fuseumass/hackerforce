from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from hackathons.models import Sponsorship, Hackathon
from companies.models import Company


def page404(request):
    return render(request, "404.html", status=404)

@login_required
def dashboard_index(request):
    if request.user.is_authenticated and request.user.current_hackathon:
        current_hackathon = request.user.current_hackathon
    else:
        messages.info(request, "You need to select a default hackathon. This is configurable on your profile page. Until this is set, the most recent hackathon will be displayed.")
        current_hackathon = Hackathon.latest()

    return redirect("dashboard:view", h_pk=current_hackathon.pk)

@login_required
def dashboard(request, h_pk):
    current_hackathon = get_object_or_404(Hackathon, pk=h_pk)

    sponsorships = Sponsorship.objects.filter(hackathon=current_hackathon).order_by(
        "updated_at"
    )
    money_raised = 0

    for sponsorship in sponsorships:
        money_raised = money_raised + sponsorship.contribution

    contacted_count = 0
    uncontacted_count = 0
    donated_count = 0
    for sp in sponsorships:
        if sp.status == Sponsorship.CONTACTED:
            contacted_count = contacted_count + 1
        elif sp.status == Sponsorship.CONFIRMED:
            donated_count = donated_count + 1
        else:
            uncontacted_count = uncontacted_count + 1

    chart = [
        ["Contacted", contacted_count],
        ["Uncontacted", uncontacted_count],
        ["Donated", donated_count],
    ]
    return render(
        request,
        "dashboard.html",
        {
            "current_hackathon": current_hackathon,
            "money_raised": money_raised,
            "sponsorships": sponsorships[:5],
            "chart_data": chart,
            "progress_bar_width": (money_raised / current_hackathon.fundraising_goal * 100),
        },
    )
