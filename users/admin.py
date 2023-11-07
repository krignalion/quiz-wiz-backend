from django.contrib import admin

from .models import UserProfile, UserRequest


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "username",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "username",
    )
    list_filter = ("created_at", "updated_at")
    list_per_page = 20


class RequestAdmin(admin.ModelAdmin):
    list_display = ("user", "company", "status")
    search_fields = ("user_username", "company__name")
    list_filter = ("status", "company")


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserRequest, RequestAdmin)
