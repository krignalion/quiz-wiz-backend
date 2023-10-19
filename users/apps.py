from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from .signals import user_profile_change, user_profile_deleted

        post_save.connect(user_profile_change, sender=self.get_model('UserProfile'))
        post_delete.connect(user_profile_deleted, sender=self.get_model('UserProfile'))
