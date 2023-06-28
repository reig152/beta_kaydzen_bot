from django.db import models


# Создадим модель создания обеспокоенности
class Concerns(models.Model):
    """Модель создания обеспокоенности."""

    # Классификатор (название) обеспокоенности
    concern_class = models.CharField(
        verbose_name="Классификатор обеспокоенности",
        max_length=40
    )

    # Описание обеспокоенности
    concern_description = models.TextField(
        verbose_name="Описание обеспокоенности"
    )

    # Предполагаемая причина (первоисточник)
    concern_reason = models.TextField(
        verbose_name="Предполагаемая причина"
    )

    # Предполагаемое решение
    concern_solution = models.TextField(
        verbose_name="Предполагаемое решение"
    )

    # Критичность обеспокоенности
    concern_importance = models.CharField(
        verbose_name="Критичность обеспокоенности"
    )

    # Дата создания обеспокоенности
    added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления в базу данных'
    )

    class Meta:
        """
        Класс для отображения модели на русском языке;
        Сортировка обеспокоенностей по дате добавления в БД.
        """
        verbose_name = 'Обеспокоенность'
        verbose_name_plural = 'Обеспокоенности'
        ordering = ['-added']

    def __str__(self) -> str:
        """
        Метод для отображения названия
        обеспокоенности в админке.
        """
        return self.concern_class
