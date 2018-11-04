from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth import login as login_auth, authenticate
from profiles.forms import RegistrationForm

def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      raw_password = form.cleaned_data.get('password1')
      user = authenticate(username=username, password=raw_password)
      login_auth(request, user)
      return redirect('home')
  else:
    form = RegistrationForm()
  return render(request, 'register.html.j2', {'form': form})

def login(request):
  return render(request, 'login.html.j2')

def settings(request):
  return render(request, 'settings.html.j2')
