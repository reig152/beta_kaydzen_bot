from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Модель отображения полей в админ панели."""
    list_display = [
        'username',
        'role',
    ]

    # Фильтрация по ролям
    list_filter = [
        'role',
    ]

    # Поиск по username
    search_fields = [
        'username',
    ]
