"""Website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include

from django.contrib import admin
from django.conf.urls import url
from profiles import views as profile_views
from dashboard import views as dashboard_views


admin.autodiscover()

from profiles.views import register, login, logout

urlpatterns = [
    path("", include("dashboard.urls")),
    path("admin/", admin.site.urls),
    path("h/", include("hackathons.urls")),
    path("global/companies/", include("companies.urls")),
    path("global/contacts/", include("contacts.urls")),
    path("email/", include("emails.urls")),
    path("settings/", include("profiles.urls")),
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    url(
        r"^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        profile_views.activate,
        name="activate",
    ),
    url(r"^.*/$", dashboard_views.page404, name="404"),
]
