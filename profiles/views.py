from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.contrib.auth import login as login_auth, authenticate, logout as logout_auth
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, AuthenticationFormWithCSS, ProfileForm

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .token import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from .models import User
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            # user = authenticate(username=username, password=raw_password)

            current_site = get_current_site(request)
            mail_subject = 'Activate your hacker-force account'
            message = render_to_string('activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            messages.info(request, "Thank you for signing up! Please check your email to activate your account.", extra_tags="info")
            return redirect('login')
            # login_auth(request, user)
            # return redirect("/")
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    return render(request, "register.html", {"form": form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login_auth(request, user)
        messages.success(request, "Thank you for confirming! You may now login.", extra_tags="success")
        return redirect('login')
    else:
        messages.error(request, "Invalid activation link!", extra_tags="danger")
        return redirect('login')

def login(request):
    if request.method == "POST":
        form = AuthenticationFormWithCSS(request.POST)
        username = request.POST.get("username")
        raw_password = request.POST.get("password")
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            login_auth(request, user)
            return redirect("/")
        else:
            messages.error(request, "Invalid username or password", extra_tags="danger")
    else:
        form = AuthenticationFormWithCSS()
    return render(request, "login.html", {"form": form})


def logout(request):
    logout_auth(request)
    return redirect("/login")

@login_required
def settings(request):
    return render(request, "settings.html")


@login_required
def profile_edit(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            messages.success(request, "Edited profile successfully")
            return redirect("profiles:edit")
    else:
        form = ProfileForm(instance=request.user)
    return render(request, "profile_edit.html", {"form": form})
