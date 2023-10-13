from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        # Import and connect signals
        from .signals import user_profile_created, user_profile_updated, user_profile_deleted

        # Connect signals to the respective functions
        post_save.connect(user_profile_created, sender=self.get_model('UserProfile'))
        post_save.connect(user_profile_updated, sender=self.get_model('UserProfile'))
        post_delete.connect(user_profile_deleted, sender=self.get_model('UserProfile'))
