from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.core.exceptions import ValidationError

from app.apps.companies.models import Company, Department


class CustomPermission(Permission):

    class Meta:
        verbose_name = "Право"
        verbose_name_plural = "Права"
        proxy = True

    def __str__(self):
        return self.get_human_readable_permission()

    def get_human_readable_permission(self):
        # Словарь для замены стандартных паттернов на человекочитаемые имена
        pattern_mapping = {
            'Can add': 'Может добавлять',
            'Can change': 'Может изменять',
            'Can delete': 'Может удалять',
            'Can view': 'Может просматривать',
            # Добавьте другие паттерны и их замены, если требуется
        }
        
        # Заменяем стандартные паттерны на человекочитаемые имена, используя словарь
        name = self.name
        for pattern, human_readable_name in pattern_mapping.items():
            name = name.replace(pattern, human_readable_name)

        return name


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(CustomPermission, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"


class CustomUser(AbstractUser):
    """Модель пользователя c учетом добавления ролей"""
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
    department_name = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        verbose_name="Департамент пользователя",
        null=True,
        blank=True
    )
    position = models.CharField(
        verbose_name="Должность пользователя",
        max_length=150,
        blank=True
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name='Роль'
    )
    custom_user_permissions = models.ManyToManyField(
        CustomPermission,
        blank=True,
        related_name='custom_users'
    )

    def __str__(self):
        """Возвращает строковое представление пользователя."""
        return self.username

    @property
    def user_permissions(self):
        return self.custom_user_permissions
    
    def is_sorter(self):
        if self.role.name == 'Сортировщик':
            return True

    def save(self, *args, **kwargs):
        # Сохраняем пользователя
        super().save(*args, **kwargs)

        # После сохранения пользователя, очищаем ManyToMany связь
        self.custom_user_permissions.clear()
        
        # Перед сохранением пользователя, убедимся, что связи с ролью и правами установлены
        if self.role:
            # Если есть роль, получаем связанные права и устанавливаем их пользователю
            permissions = self.role.permissions.all()
            self.custom_user_permissions.set(permissions)

        # Сохраняем пользователя с установленными связями
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
