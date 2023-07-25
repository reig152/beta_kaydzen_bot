from django.apps import AppConfig

from django.db.models.signals import post_migrate


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.apps.users"
    verbose_name = "Управление пользователями"

    def ready(self):
        from .signals import create_default_roles
        post_migrate.connect(create_default_roles, sender=self)
