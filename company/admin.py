from django.contrib import admin

from .models import Company, Invitation


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")
    search_fields = ("name", "description")
    list_filter = ("created_at", "updated_at")
    list_per_page = 20


class InvitationAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "company", "status")
    search_fields = ("sender__username", "receiver__username", "company__name")
    list_filter = ("status", "company")


admin.site.register(Company, CompanyAdmin)
admin.site.register(Invitation, InvitationAdmin)
