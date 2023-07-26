from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages

from .concern_types import ConcernTypes
from app.apps.companies.models import Company
from app.apps.users.models import CustomUser, Role


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


class ConcernHandle(models.Model):
    """Модель решения обеспокоенностей."""
    responsible_user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Ответственный пользователь',
    )
    concern = models.OneToOneField(
        Concerns,
        on_delete=models.CASCADE,
        verbose_name='Обеспокоенность'
    )
    solution = models.TextField(
        null=True,
        blank=True,
        verbose_name='Описание решения'
    )

    class Meta:
        verbose_name = 'Решение'
        verbose_name_plural = 'Решения'

    def __str__(self):
        return f"Решение для {self.concern}"


@receiver(post_save, sender=Concerns)
def create_concern_handle(sender, instance, created, **kwargs):
    """
    Функция-обработчик сигнала post_save для модели Concerns.
    Создает запись в модели ConcernHandle при создании обеспокоенности.
    """
    if created:
        # Если обеспокоенность была только что создана, создаем запись в модели ConcernHandle
        ConcernHandle.objects.create(concern=instance)

        # Отправляем уведомление для пользователей с ролью "Сортировщик"
        send_concern_created_notification(instance)


@receiver(post_save, sender=Concerns)
def send_concern_created_notification(concern_instance, **kwargs):
    """
    Функция для отправки уведомления
    o создании обеспокоенности для пользователей
    c ролью "Сортировщик".
    """
    # Получаем роли всех пользователей, связанных с обеспокоенностью
    roles = Role.objects.filter(users__concern=concern_instance)

    # Фильтруем роли, чтобы получить только пользователей с ролью "Сортировщик"
    sorters = roles.filter(name='Сортировщик')

    # Получаем список пользователей с ролью "Сортировщик"
    sorter_users = sorters.values_list('users__username', flat=True)

    # Отправляем уведомление для каждого пользователя с ролью "Сортировщик"
    for username in sorter_users:
        messages.add_message(
            request=None,  # Этот аргумент не требуется, так как мы отправляем уведомление в админ-панели
            level=messages.INFO,  # Уровень уведомления INFO (зеленый)
            message=f"Новая обеспокоенность создана: {concern_instance}",  # Сообщение с информацией о созданной обеспокоенности
        )
