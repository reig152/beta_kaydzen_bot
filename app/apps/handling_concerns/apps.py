from django.apps import AppConfig

from django.db.models.signals import post_migrate

class HandlingConcernsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.apps.handling_concerns"
    verbose_name = "Управление обеспокоенностями"

    def ready(self):
        from .signals import create_default_statuses
        post_migrate.connect(create_default_statuses, sender=self)
