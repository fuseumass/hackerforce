from django.contrib import admin

from emails.models import Email

# Register your models here.

@admin.register(Email)
class emailAdmin(admin.ModelAdmin):
    list_display = ('subject','messageText', 'messageStatus','lastUpdate', 'modifiedBy')
