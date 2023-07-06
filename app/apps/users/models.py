from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

from app.apps.companies.models import Company


class CustomUser(AbstractUser):
    """Модель пользователя с учетом добавления ролей"""
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=150,
        blank=True
    )
    middle_name = models.CharField(
        verbose_name="Отчество",
        max_length=150,
        blank=True
    )
    email = models.EmailField(
        verbose_name="Email",
        blank=True
    )
    mobile = models.CharField(
        verbose_name="Телефон",
        max_length=150,
        blank=True
    )
    telegram_username = models.CharField(
        unique=True,
        null=True,
        blank=True,
        max_length=40,
        verbose_name="Telegram username"
    )
    company_name = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Компания пользователя",
        null=True,
        blank=True
    )
    position = models.CharField(
        verbose_name="Должность пользователя",
        max_length=150,
        blank=True
    )

    def __str__(self):
        """Возвращает строковое представление пользователя."""
        return self.username

    def clean(self):
        """
        Метод для выполнения дополнительной валидации модели.
        Если имя пользователя (username) равно "me",
        будет вызвано исключение ValidationError.
        """
        if self.username == 'me':
            raise ValidationError('Запрещено использовать me '
                                  'в качестве username!')

    def save(self, *args, **kwargs):
        """
        Переопределенный метод save(), который вызывает метод full_clean()
        для валидации модели перед сохранением в базу данных,
        а затем вызывает оригинальный метод save() базовой модели.
        """
        self.full_clean()
        return super().save(*args, **kwargs)
