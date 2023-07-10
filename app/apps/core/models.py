from django.db import models

from app.apps.users.models import CustomUser


class TGUser(models.Model):
    id = models.BigIntegerField(
        primary_key=True,
        verbose_name="Telegram User ID",
        blank=True
    )
    chat_id = models.BigIntegerField(
        verbose_name="Telegram Chat ID",
        blank=True
    )
    username = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Имя пользователя telegram"
    )

    objects: models.manager.BaseManager["TGUser"]

    class Meta:
        db_table = "tg_user"
    
    def __str__(self) -> str:
        return self.username.username
