from django.contrib import admin
from .models import CustomUser

from app.apps.companies.models import Company


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

    # Поиск по username
    search_fields = [
        'username',
    ]

    def get_queryset(self, request):
        """
        Метод, фильтрующий пользователей по компаниям.
        """
        queryset = super().get_queryset(request)

        if not request.user.is_superuser:
            # Получаем все компании, связанные с пользователем
            user_companies = Company.objects.filter(customuser__id=request.user.id)
            # Получаем все названия обеспокоенностей, связанные с компаниями пользователя
            queryset = queryset.filter(company_name__in=user_companies)
        return queryset

    def get_form(self, request, obj=None, **kwargs):
        """
        Метод, который предоставляет выбор для редактирования
        компаний сотрудников.
        """
        form = super().get_form(request, obj, **kwargs)
        # выполняется проверка на права пользователя
        if not request.user.is_superuser and request.user.has_perm(
            'users.change_customuser'
        ):
            # Ограничиваем выбор только классификаторами, связанными с компаниями пользователя
            form.base_fields['company_name'].queryset = Company.objects.filter(
                customuser__id=request.user.id
            )
        return form
