from django.contrib import admin
from .models import Concerns


@admin.register(Concerns)
class ConcernsAdmin(admin.ModelAdmin):
    """Модель отображения полей в админ панели."""
    list_display = [
        'concern_class',
        'concern_description',
        'concern_reason',
        'concern_solution',
        'concern_importance',
        'added',
    ]

    # Поле даты добавления изменять нельзя
    readonly_fields = ['added']

    # Фильтрация по названию и важности обеспокоенности
    list_filter = [
        'concern_class',
        'concern_importance',
    ]
