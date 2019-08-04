from django.urls import path

from . import views

app_name = 'emails'

urlpatterns = [
    path("h/<int:h_pk>/emails/<int:pk>", views.email_detail, name="view"),
    path("h/<int:h_pk>/emails/<int:pk>/render", views.render_message, name="render"),
    path("h/<int:h_pk>/emails/<int:pk>/edit", views.email_edit, name="edit"),
    path("h/<int:h_pk>/emails/drafts", views.drafts, name="drafts"),
    path("h/<int:h_pk>/emails/sent", views.sent, name="sent"),
    path("h/<int:h_pk>/emails/compose", views.emails, name="compose"),
    path("h/<int:h_pk>/emails/compose/from_contacts", views.compose_from_contacts, name="compose_from_contacts"),
    path("h/<int:h_pk>/emails/compose/from_company", views.compose_from_company, name="compose_from_company"),
    path("h/<int:h_pk>/emails/compose/from_industry", views.compose_from_industry, name="compose_from_industry")
]