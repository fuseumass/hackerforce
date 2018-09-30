from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard.html')

def contacts(request):
    return render(request, 'contacts.html')

def companies(request):
    return render(request, 'companies.html')

def email(request):
    return render(request, 'email.html')

def drafts(request):
    return render(request, 'emailDrafts.html')

def sent(request):
    return render(request, 'sentEmails.html')

def outbox(request):
    return render(request, 'outbox.html')

def settings(request):
    return render(request, 'settings.html')
