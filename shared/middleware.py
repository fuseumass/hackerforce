from django.shortcuts import get_object_or_404
from django.contrib import messages
from hackathons.models import Hackathon

class CurrentHackathonMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        pk = view_kwargs.get('h_pk', None)
        if pk:
            request.hackathon = get_object_or_404(Hackathon, pk=pk)
