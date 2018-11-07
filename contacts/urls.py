from django.urls import path

from . import views

app_name = "contacts"
urlpatterns = [
    path("", views.contacts, name="index"),
    path("new", views.contact_new, name="new"),
    path("<int:pk>/edit", views.contact_edit, name="edit"),
]
