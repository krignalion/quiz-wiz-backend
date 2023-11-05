from django.contrib import admin

from company.models import Invitation
from users.models import UserRequest


class InvitationAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "company", "status")
    search_fields = ("sender__username", "receiver__username", "company__name")
    list_filter = ("status", "company")


class RequestAdmin(admin.ModelAdmin):
    list_display = ("user", "company", "status")
    search_fields = ("user_username", "company__name")
    list_filter = ("status", "company")


admin.site.register(Invitation, InvitationAdmin)
admin.site.register(UserRequest, RequestAdmin)
