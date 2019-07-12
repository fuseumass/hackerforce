from django.urls import path, include

from .views import hackathons, perks, sponsorships, leads, tiers

urlpatterns_tiers = [
    path("tiers/new", tiers.tier_new, name="new"),
    path("tiers/<int:pk>/edit", tiers.tier_edit, name="edit"),
    path("<int:h_pk>/tiers/<int:pk>", tiers.tier_detail, name="view"),
]

urlpatterns_perks = [
    path("perks/new", perks.perk_new, name="new"),
    path("perks/<int:pk>/edit", perks.perk_edit, name="edit"),
    path("<int:h_pk>/perks/<int:pk>", perks.perk_detail, name="view"),
]

urlpatterns_sponsorships = [
    path("<int:h_pk>/sponsorships", sponsorships.sponsorships_show, name="show"),
    path("<int:h_pk>/sponsorships/<int:pk>/edit", sponsorships.sponsorship_edit, name="edit"),
    path("<int:h_pk>/sponsorships/<int:pk>/delete", sponsorships.sponsorship_delete, name="delete"),
    path("<int:h_pk>/sponsorships/<int:pk>", sponsorships.sponsorship_detail, name="view"),
    path("<int:h_pk>/sponsorships/new", sponsorships.sponsorship_new, name="new"),
]

urlpatterns_leads = [
    path("<int:h_pk>/leads", leads.leads_show, name="show"),
    path("<int:h_pk>/leads/<int:pk>/edit", leads.lead_edit, name="edit"),
    path("<int:h_pk>/leads/<int:pk>/delete", leads.lead_delete, name="delete"),
    path("<int:h_pk>/leads/<int:pk>", leads.lead_detail, name="view"),
    path("<int:h_pk>/leads/new", leads.lead_new, name="new"),
    path("<int:h_pk>/leads/mark_contacted/<int:c_pk>", leads.lead_mark_contacted, name="mark_contacted"),
]

app_name = "hackathons"
urlpatterns = [
    path("", include((urlpatterns_tiers, "tiers"))),
    path("", include((urlpatterns_perks, "perks"))),
    path("", include((urlpatterns_sponsorships, "sponsorships"))),
    path("", include((urlpatterns_leads, "leads"))),

    path("", hackathons.hackathons, name="index"),
    path("new", hackathons.hackathon_new, name="new"),
    path("<int:h_pk>/edit", hackathons.hackathon_edit, name="edit"),
]
