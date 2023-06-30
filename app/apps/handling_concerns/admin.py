from django.contrib import admin
from .models import (
    Concerns, ConcernName,
    ConcernImportance, ConcernStatus,
    ConcernUrgency
)


# произведем регистрацию 3 одинаковых моделей
@admin.register(
    ConcernImportance, ConcernStatus, ConcernUrgency
)
class ModelAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'description'
    ]


# регистрация названия обеспокоенностей
@admin.register(ConcernName)
class ConcernNameAdmin(admin.ModelAdmin):
    """
    Модель отображения названий
    обеспокоенностей в админ панели.
    """
    list_display = [
        'pk',
        'company_name',
        'description'
    ]


# регистрация самих обеспокоенностей
@admin.register(Concerns)
class ConcernsAdmin(admin.ModelAdmin):
    """
    Модель отображения
    обеспокоенностей в админ панели.
    """
    list_display = [
        'pk',
        'added_by',
        'concern_name',
        'concern_urgency',
        'concern_importance',
        'concern_status',
        'concern_description',
        'concern_reason',
        'concern_solution',
        'added',
    ]

    # Поле даты добавления изменять нельзя
    readonly_fields = ['added', 'added_by']

    def save_model(self, request, obj, form, change):
        # метод устанавливает, какой пользователь добавил обеспокоенность
        # через панель администратора
        if not obj.added_by_id:
            # Если поле added_by не заполнено, установите его в текущего пользователя
            obj.added_by = request.user
        super().save_model(request, obj, form, change)
