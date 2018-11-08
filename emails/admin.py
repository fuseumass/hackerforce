from django.contrib import admin

from emails.models import Email

# Register your models here.


@admin.register(Email)
class emailAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "body",
        "status",
        "time_sent",
        "last_update",
        "created_by",
    )
