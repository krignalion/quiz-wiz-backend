from django.contrib import admin

from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at", "updated_at")
    search_fields = ("name", "description")
    list_filter = ("created_at", "updated_at")
    list_per_page = 20


admin.site.register(Company, CompanyAdmin)
