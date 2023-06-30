from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Модель отображения полей в админ панели."""
    list_display = [
        'pk',
        'username',
        'telegram_username',
        'company_name',
    ]

    # Фильтрация по ролям
    list_filter = [
        'company_name',
    ]

    list_editable = [
        'company_name',
    ]

    # Поиск по username
    search_fields = [
        'username',
    ]
