from django.urls import path

from .views import hackathons, perks, sponsorships, tiers

app_name = "hackathons"
urlpatterns = [
    path("", hackathons.hackathons, name="index"),
    path("new", hackathons.hackathon_new, name="hackathon_new"),
    path("tiers/new", tiers.tier_new, name="tier_new"),
    path("tiers/<int:pk>/edit", tiers.tier_edit, name="tier_edit"),
    path("perks/new", perks.perk_new, name="perk_new"),
    path("perks/<int:pk>/edit", perks.perk_edit, name="perk_edit"),
    path("sponsorships/new", sponsorships.sponsorship_new, name="sponsorship_new"),
    #################
    # Per-hackathon #
    path("<int:h_pk>/edit", hackathons.hackathon_edit, name="hackathon_edit"),
    path("<int:h_pk>/sponsorships", sponsorships.sponsorships_show, name="sponsorships_show"),
    path("<int:h_pk>/sponsorships/<int:pk>/edit", sponsorships.sponsorship_edit, name="sponsorship_edit"),
    path("<int:h_pk>/sponsorships/<int:pk>", sponsorships.sponsorship_detail, name="sponsorship_detail"),
    path("<int:h_pk>/sponsorships", sponsorships.sponsorships_show, name="sponsorships_show"),
]
