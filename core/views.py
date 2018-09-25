from django.shortcuts import render

def index(request):
    return render(request, 'index.jinja')

def contacts(request):
    return render(request, 'contacts.jinja')

def companies(request):
    return render(request, 'companies.jinja')

def email(request):
    return render(request, 'email.jinja')
