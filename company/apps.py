from django.apps import AppConfig
from django.db.models.signals import post_delete, post_save


class CompanyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "company"

    def ready(self):
        from .signals import company_created, company_deleted, company_updated

        post_save.connect(company_created, sender=self.get_model("Company"))
        post_save.connect(company_updated, sender=self.get_model("Company"))
        post_delete.connect(company_deleted, sender=self.get_model("Company"))
