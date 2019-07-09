from django.urls import path

from . import views

app_name = 'emails'

urlpatterns = [
    path("h/<int:h_pk>/emails/view/<int:pk>", views.email_detail, name="view"),
    path("h/<int:h_pk>/emails/drafts", views.drafts, name="drafts"),
    path("h/<int:h_pk>/emails/sent", views.sent, name="sent"),
    path("h/<int:h_pk>/emails/compose", views.emails, name="compose"),
    path("h/<int:h_pk>/emails/compose1", views.compose1, name="compose1"),
    path("h/<int:h_pk>/emails/compose2", views.compose2, name="compose2"),
    path("h/<int:h_pk>/emails/compose3", views.compose3, name="compose3")
]