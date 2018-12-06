from django.contrib import admin
from .models import Tier, Perk, Hackathon, Sponsorship

# Register your models here.

admin.site.register(Tier)
admin.site.register(Perk)
admin.site.register(Hackathon)
admin.site.register(Sponsorship)
