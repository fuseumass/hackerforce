from django.urls import path

from . import views

app_name = 'emails'
urlpatterns = [
    path("", views.emails, name="index"),
    path("drafts", views.drafts, name="drafts"),
    path("outbox", views.outbox, name="outbox"),
    path("sent", views.sent, name="sent"),
    path("<int:pk>/edit", views.email_edit, name="edit"),
     path("<int:pk>/sent_view", views.sent_view, name="sent_view"),
]