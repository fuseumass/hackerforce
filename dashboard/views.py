from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from hackathons.models import Sponsorship, Hackathon, Lead
from companies.models import Company
from contacts.models import Contact


def page404(request):
    return render(request, "404.html", status=404)

@login_required
def dashboard_index(request):
    if request.user.is_authenticated and request.user.current_hackathon:
        current_hackathon = request.user.current_hackathon
    else:
        messages.info(request, "You need to select a default hackathon. This is configurable on your profile page. Until this is set, the most recent hackathon will be displayed.")
        current_hackathon = Hackathon.latest()
        if not current_hackathon:
            return redirect("hackathons:index")

    return redirect("dashboard:view", h_pk=current_hackathon.pk)

@login_required
def dashboard(request, h_pk):
    current_hackathon = get_object_or_404(Hackathon, pk=h_pk)

    sponsorships = Sponsorship.objects.filter(hackathon=current_hackathon).order_by("-updated_at").select_related()
    money_raised = 0
    money_expected = 0
    money_possible = 0

    for sponsorship in sponsorships:
        if sponsorship.status == Sponsorship.PAID:
            money_raised += sponsorship.contribution
        elif sponsorship.status == Sponsorship.CONFIRMED:
            money_expected += sponsorship.contribution
        elif sponsorship.status == Sponsorship.RESPONDED:
            money_possible += sponsorship.contribution

    goal = current_hackathon.fundraising_goal
    money_raised_width = min(money_raised / goal * 100, goal)
    money_expected_width = max(0, min(money_expected / goal * 100, goal - money_raised))
    money_possible_width = max(0, min(money_possible / goal * 100, goal - money_raised - money_possible))

    money_expected += money_raised
    money_possible += money_expected
    
    sponsorship_chart = gen_sponsorship_chart(sponsorships, current_hackathon)

    leads = Lead.objects.filter(sponsorship__hackathon=current_hackathon).order_by("-updated_at").select_related()
    lead_chart = gen_lead_chart(leads, current_hackathon)

    your_sponsorships = Sponsorship.objects.filter(hackathon=current_hackathon, organizer_contacts=request.user)

    return render(
        request,
        "dashboard.html",
        {
            "current_hackathon": current_hackathon,
            "sponsorships": sponsorships[:10],
            "sponsorship_chart_data": sponsorship_chart,
            "leads": leads[:10],
            "lead_chart_data": lead_chart,
            "money_raised": money_raised,
            "money_expected": money_expected,
            "money_possible": money_possible,
            "money_raised_width": money_raised_width,
            "money_expected_width": money_expected_width,
            "money_possible_width": money_possible_width,
            "your_sponsorships": your_sponsorships,
        },
    )

def gen_lead_chart(leads, hackathon):
    responded_count = 0
    contacted_count = 0
    ghosted_count = 0
    for l in leads:
        if l.status in [Lead.RESPONDED]:
            responded_count += 1
        elif l.status in [Lead.CONTACTED]:
            contacted_count += 1
        elif l.status in [Lead.GHOSTED]:
            ghosted_count += 1

    uncontacted_count = Contact.objects.exclude(leads__sponsorship__hackathon=hackathon).count()
    return [
        ["Responded", responded_count, "responded", "green"],
        ["Contacted", contacted_count, "contacted", "orange"],
        ["Uncontacted", uncontacted_count, "uncontacted", "gray-dark"],
        ["Ghosted", ghosted_count, "dead", "pink"],
    ]

def gen_sponsorship_chart(sponsorships, hackathon):
    confirmed_count = 0
    progress_count = 0
    dead_count = 0
    for sp in sponsorships:
        if sp.status in [Sponsorship.CONFIRMED, Sponsorship.PAID]:
            confirmed_count += 1
        elif sp.status in [Sponsorship.ASSIGNED, Sponsorship.CONTACTED, Sponsorship.RESPONDED]:
            progress_count += 1
        elif sp.status in [Sponsorship.DENIED, Sponsorship.GHOSTED]:
            dead_count += 1

    uncontacted_count = Company.objects.exclude(sponsorships__hackathon=hackathon).count()
    return [
        ["Confirmed", confirmed_count, "confirmed", "green"],
        ["In Progress", progress_count, "in_progress", "orange"],
        ["Uncontacted", uncontacted_count, "uncontacted", "gray-dark"],
        ["Dead", dead_count, "dead", "pink"],
    ]