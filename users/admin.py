from django.contrib import admin

from .models import UserProfile


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


admin.site.register(UserProfile, UserProfileAdmin)
