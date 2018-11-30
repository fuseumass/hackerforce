from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from hackathons.models import Sponsorship, Hackathon

# @login_required
def dashboard(request):
  current_hackathon = Hackathon.objects.latest('date')
  sponsorships = Sponsorship.objects.filter(hackathon=current_hackathon)
  money_raised = 0
  for sponsorship in sponsorships:
    money_raised = money_raised + sponsorship.contribution
  return render(request, 'dashboard.html.j2', {"current_hackathon":current_hackathon, "money_raised":money_raised})