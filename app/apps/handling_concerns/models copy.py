# from django.db import models

# from app.apps.users.models import CustomUser


# # установим 3 уровня обеспокоенности для выбора
# CHOICES_IMPORTANCE = (
#         ('low', 'Низкая обеспокоенность'),
#         ('medium', 'Средняя обеспокоенность'),
#         ('high', 'Высокая обеспокоенность'),
#     )


# class ConcernName(models.Model):
#     # Классификатор (название) обеспокоенности
#     title = models.CharField(
#         verbose_name="Классификатор обеспокоенности",
#         max_length=40
#     )

#     class Meta:
#         verbose_name = 'Название обеспокоенности'
#         verbose_name_plural = 'Названия обеспокоенностей'

#     def __str__(self) -> str:
#         return self.title


# # Создадим модель создания обеспокоенности
# class Concerns(models.Model):
#     """Модель создания обеспокоенности."""

#     # Классификатор (название) обеспокоенности
#     concern_name = models.ForeignKey(
#         ConcernName,
#         # При удалении названия, запись не удалится
#         on_delete=models.SET_NULL,
#         verbose_name="Классификатор обеспокоенности",
#         null=True
#     )

#     # Описание обеспокоенности
#     concern_description = models.TextField(
#         verbose_name="Описание обеспокоенности"
#     )

#     # Предполагаемая причина (первоисточник)
#     concern_reason = models.TextField(
#         verbose_name="Предполагаемая причина"
#     )

#     # Предполагаемое решение
#     concern_solution = models.TextField(
#         verbose_name="Предполагаемое решение"
#     )

#     # Критичность обеспокоенности
#     concern_importance = models.CharField(
#         # используем установленные выше
#         # уровни обеспокоенности
#         choices=CHOICES_IMPORTANCE,
#         verbose_name="Критичность обеспокоенности"
#     )

#     # Дата создания обеспокоенности
#     added = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name='Дата добавления в базу данных'
#     )

#     added_by = models.ForeignKey(
#         CustomUser,
#         on_delete=models.CASCADE,
#         verbose_name="Автор обеспокоенности"
#     )

#     class Meta:
#         """
#         Класс для отображения модели на русском языке;
#         Сортировка обеспокоенностей по дате добавления в БД.
#         """
#         verbose_name = 'Обеспокоенность'
#         verbose_name_plural = 'Обеспокоенности'
#         ordering = ['-added']

#     def __str__(self) -> str:
#         """
#         Метод для отображения названия
#         обеспокоенности в админке.
#         """
#         return self.concern_name
