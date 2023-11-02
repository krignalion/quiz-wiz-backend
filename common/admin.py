from django.contrib import admin

from .models import Invitation, Request


class InvitationAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "company", "status")
    search_fields = ("sender__username", "receiver__username", "company__name")
    list_filter = ("status", "company")


class RequestAdmin(admin.ModelAdmin):
    list_display = ("user", "company", "status")
    search_fields = ("user_username", "company__name")
    list_filter = ("status", "company")


admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Request, RequestAdmin)
