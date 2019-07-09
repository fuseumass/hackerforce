from django.urls import path

from . import views

app_name = 'emails'

urlpatterns = [
    path("h/<int:h_pk>/view/<int:pk>", views.email_detail, name="view"),
    path("h/<int:h_pk>/drafts", views.drafts, name="drafts"),
    path("h/<int:h_pk>/sent", views.sent, name="sent"),
    path("h/<int:h_pk>/compose", views.emails, name="compose"),
    path("h/<int:h_pk>/compose1", views.compose1, name="compose1"),
    path("h/<int:h_pk>/compose2", views.compose2, name="compose2"),
    path("h/<int:h_pk>/compose3", views.compose3, name="compose3")
]