from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


CHOICES_ROLE = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
    ('kaizen_admin', 'kaizen_admin')
)


class CustomUser(AbstractUser):
    """Модель пользователя с учетом добавления ролей"""
    name = models.TextField(
        null=True,
        blank=True,
        verbose_name="Имя пользователя"
    )
    surname = models.TextField(
        null=True,
        blank=True,
        verbose_name="Фамилия пользователя"
    )
    username = models.CharField(
        unique=True,
        max_length=40,
        verbose_name="Telegram username"
    )
    role = models.CharField(
        max_length=32,
        choices=CHOICES_ROLE,
        default='user'
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


    # Методы, которые проверяют текущую роль пользователя
    # возвращают True или False в зависимости от соответствия роли.
    def is_user(self):
        if self.role == 'user':
            return True
        return False

    def is_moderator(self):
        if self.role == 'moderator':
            return True
        return False

    def is_admin(self):
        if self.role == 'admin':
            return True
        return False
    
    def is_kaizen_admin(self):
        if self.role == 'kaizen_admin':
            return True
        return False
