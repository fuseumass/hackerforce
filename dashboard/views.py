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
    money_expected = 0
    money_possible = 0

    for sponsorship in sponsorships:
        if sponsorship.status == Sponsorship.PAID:
            money_raised += sponsorship.contribution
        elif sponsorship.status == Sponsorship.CONFIRMED:
            money_expected += sponsorship.contribution
        else:
            money_possible += sponsorship.contribution

    goal = current_hackathon.fundraising_goal
    money_raised_width = min(money_raised / goal * 100, goal)
    money_expected_width = max(0, min(money_expected / goal * 100, goal - money_raised))
    money_possible_width = max(0, min(money_possible / goal * 100, goal - money_raised - money_possible))

    money_expected += money_raised
    money_possible += money_expected

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
            "sponsorships": sponsorships[:5],
            "chart_data": chart,
            "money_raised": money_raised,
            "money_expected": money_expected,
            "money_possible": money_possible,
            "money_raised_width": money_raised_width,
            "money_expected_width": money_expected_width,
            "money_possible_width": money_possible_width,
        },
    )
