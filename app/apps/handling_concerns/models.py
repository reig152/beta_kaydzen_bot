from django.db import models

from .concern_types import ConcernTypes
from app.apps.companies.models import Company
from app.apps.users.models import CustomUser


class ConcernName(ConcernTypes):
    # Классификатор (название) обеспокоенности
    company_name = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        verbose_name="Название компании",
        null=True,
        blank=True
    )

    class Meta:
        """
        Класс для отображения модели на русском языке.
        """
        verbose_name = "Классификатор обеспокоенности"
        verbose_name_plural = "Классификаторы обеспокоенностей"



class ConcernUrgency(ConcernTypes):
    """Модель срочности обеспокоенности."""
    class Meta:
        """
        Класс для отображения модели на русском языке.
        """
        verbose_name = "Срочность обеспокоенности"
        verbose_name_plural = "Срочность обеспокоенностей"


class ConcernImportance(ConcernTypes):
    """Модель критичности обеспокоенности."""
    class Meta:
        """
        Класс для отображения модели на русском языке.
        """
        verbose_name = "Критичность обеспокоенности"
        verbose_name_plural = "Критичность обеспокоенностей"


class ConcernStatus(ConcernTypes):
    """Модель статуса обеспокоенности."""
    description = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        default='В процессе исполнения',
        verbose_name='Описание'
    )
    solution = models.TextField(
        null=True,
        blank=True,
        verbose_name="Решение обеспокоенности"
    )

    class Meta:
        """
        Класс для отображения модели на русском языке.
        """
        verbose_name = "Статус обеспокоенности"
        verbose_name_plural = "Статусы обеспокоенностей"


# Создадим модель создания обеспокоенности
class Concerns(models.Model):
    """Модель создания обеспокоенности."""

    # Автор обеспокоенности
    added_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Автор обеспокоенности"
    )

    # Классификатор (название) обеспокоенности
    concern_name = models.ForeignKey(
        ConcernName,
        # При удалении названия, запись не удалится
        on_delete=models.SET_NULL,
        verbose_name="Классификатор обеспокоенности",
        null=True
    )

    # Срочность обеспокоенности
    concern_urgency = models.ForeignKey(
        ConcernUrgency,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Срочность обеспокоенности"
    )

    # Критичность обеспокоенности
    concern_importance = models.ForeignKey(
        ConcernImportance,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Критичность обеспокоенности"
    )

    # Статус обеспокоенности
    concern_status = models.ForeignKey(
        ConcernStatus,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Статус обеспокоенности"
    )

    # Наименование
    concern_title = models.CharField(
        max_length=256,
        verbose_name="Наименование обеспокоенности",
        null=True,
        blank=True
    )

    # Описание обеспокоенности
    concern_description = models.TextField(
        verbose_name="Описание обеспокоенности"
    )

    # Экономический эффект
    concern_effect = models.CharField(
        max_length=256,
        verbose_name="Экономический эффект",
        null=True,
        blank=True
    )

    # Предполагаемая причина (первоисточник)
    concern_reason = models.TextField(
        verbose_name="Предполагаемая причина"
    )

    # Предполагаемое решение
    concern_solution = models.TextField(
        verbose_name="Предполагаемое решение"
    )

    # Дата создания обеспокоенности
    added = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления в базу данных"
    )

    class Meta:
        """
        Класс для отображения модели на русском языке;
        Сортировка обеспокоенностей по дате добавления в БД.
        """
        verbose_name = "Зарегистированная обеспокоенность"
        verbose_name_plural = "Зарегистированные обеспокоенности"
        ordering = ['-added']

    def __str__(self) -> str:
        """
        Метод для отображения названия
        обеспокоенности в админке.
        """
        return self.concern_description[:20]
