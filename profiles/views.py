from django.shortcuts import render
from django.views.generic.edit import CreateView

def register(request):
    return render(request, 'register.html.j2')

def login(request):
    return render(request, 'login.html.j2')

def settings(request):
    return render(request, 'settings.html.j2')
