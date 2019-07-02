from django.urls import path, include

from .views import hackathons, perks, sponsorships, tiers

urlpatterns_tiers = [
    path("new", tiers.tier_new, name="new"),
    path("<int:pk>/edit", tiers.tier_edit, name="edit"),
]

urlpatterns_perks = [
    path("new", perks.perk_new, name="new"),
    path("<int:pk>/edit", perks.perk_edit, name="edit"),
]

urlpatterns_sponsorships = [
    path("<int:h_pk>/sponsorships", sponsorships.sponsorships_show, name="show"),
    path("<int:h_pk>/sponsorships/<int:pk>/edit", sponsorships.sponsorship_edit, name="edit"),
    path("<int:h_pk>/sponsorships/<int:pk>", sponsorships.sponsorship_detail, name="view"),
    path("<int:h_pk>/sponsorships/new", sponsorships.sponsorship_new, name="new"),
]

app_name = "hackathons"
urlpatterns = [
    path("tiers/", include((urlpatterns_tiers, "tiers"))),
    path("perks/", include((urlpatterns_perks, "perks"))),
    path("", include((urlpatterns_sponsorships, "sponsorships"))),

    path("", hackathons.hackathons, name="index"),
    path("new", hackathons.hackathon_new, name="new"),
    path("<int:h_pk>/edit", hackathons.hackathon_edit, name="edit"),
]
