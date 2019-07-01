from django.contrib import messages
from hackathons.models import Hackathon

def fill_current_hackathon_as_h(request):
    h = None
    try:
        h = request.hackathon
    except AttributeError:
        pass
    return {"h": h}