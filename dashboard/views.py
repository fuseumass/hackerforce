from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from hackathons.models import Sponsorship, Hackathon
from companies.models import Company


def page404(request):
    return render(request, "404.html", status=404)


@login_required
def dashboard(request):
    if request.user.is_authenticated and request.user.current_hackathon:
        current_hackathon = request.user.current_hackathon
    else:
        current_hackathon = Hackathon.latest()

    sponsorships = Sponsorship.objects.filter(hackathon=current_hackathon).order_by(
        "updated_at"
    )
    money_raised = 0

    for sponsorship in sponsorships:
        money_raised = money_raised + sponsorship.contribution

    companies = Company.objects.all()
    contacted_count = 0
    uncontacted_count = 0
    donated_count = 0
    for company in companies:
        if company.status == "C":
            contacted_count = contacted_count + 1
        elif company.status == "D":
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
