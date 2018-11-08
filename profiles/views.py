from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth import login as login_auth, authenticate, logout as logout_auth
from django.contrib.auth.decorators import login_required
from profiles.forms import RegistrationForm, AuthenticationFormWithInactives

def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      raw_password = form.cleaned_data.get('password1')
      user = authenticate(username=username, password=raw_password)
      login_auth(request, user)
      return redirect('/')
    else:
      print(form.errors)
  else:
    form = RegistrationForm()
  return render(request, 'register.html.j2', {'form': form})

def login(request):
  if request.method == 'POST':
    form = AuthenticationFormWithInactives(request.POST)
    username = request.POST.get('username')
    raw_password = request.POST.get('password')
    user = authenticate(username=username, password=raw_password)
    if user is not None:
      login_auth(request, user)
      return redirect('/')
  else:
    form = AuthenticationFormWithInactives()
  return render(request, 'login.html.j2', {'form': form})

def logout(request):
  logout_auth(request)
  return redirect('/login')

@login_required
def settings(request):
  return render(request, 'settings.html.j2')
