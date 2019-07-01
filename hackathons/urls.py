from django.urls import path

from . import views

app_name = "hackathons"
urlpatterns = [
    path("", views.hackathons, name="index"),
    path("new", views.hackathon_new, name="hackathon_new"),
    path("tiers/new", views.tier_new, name="tier_new"),
    path("tiers/<int:pk>/edit", views.tier_edit, name="tier_edit"),
    path("perks/new", views.perk_new, name="perk_new"),
    path("perks/<int:pk>/edit", views.perk_edit, name="perk_edit"),
    path("sponsorships/new", views.sponsorship_new, name="sponsorship_new"),
    #################
    # Per-hackathon #
    path("<int:h_pk>/edit", views.hackathon_edit, name="hackathon_edit"),
    path("<int:h_pk>/sponsorships", views.sponsorships_show, name="sponsorships_show"),
    path("<int:h_pk>/sponsorships/<int:pk>/edit", views.sponsorship_edit, name="sponsorship_edit"),
    path("<int:h_pk>/sponsorships/<int:pk>", views.sponsorship_detail, name="sponsorship_detail")
]
