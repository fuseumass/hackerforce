from django.contrib import admin

from emails.models import Email

# Register your models here.

admin.site.register(Email)
# @admin.register(Email)
# class emailAdmin(admin.ModelAdmin):
#     list_display = (
#         "company",
#         "subject",
#         "body",
#         "status",
#         "time_sent",
#         "last_update",
#         "created_by",
#     )
