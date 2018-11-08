from django.shortcuts import render
from companies.models import Company

def new(request):
    return render(request, 'new.html.j2')

def companies(request):
    companies = Company.objects.all()
    return render(request, 'companies.html.j2', context = {'companies' : companies})
