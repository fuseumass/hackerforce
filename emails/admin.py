from django.contrib import admin

from emails.models import Email

# Register your models here.

@admin.register(Email)
class emailAdmin(admin.ModelAdmin):
    list_display = ('subject','message_text', 'message_status', 'time_scheduled', 'last_update', 'modified_by')
