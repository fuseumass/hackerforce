from django.urls import path
from django.conf.urls import url

from . import views

app_name = "profiles"
urlpatterns = [
    path("", views.settings, name="settings"),
    path("edit", views.profile_edit, name="edit"),
]
