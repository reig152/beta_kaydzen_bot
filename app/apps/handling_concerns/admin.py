from django.contrib import admin
from .models import (
    Concerns, ConcernName,
    ConcernImportance, ConcernStatus,
    ConcernUrgency, ConcernHandle
)

from app.apps.companies.models import Company
from app.apps.users.models import CustomUser

from guardian.admin import GuardedModelAdmin


# произведем регистрацию 3 одинаковых моделей
@admin.register(
    ConcernImportance, ConcernStatus, ConcernUrgency
)
class ModelAdmin(GuardedModelAdmin):
    list_display = [
        'pk',
        'description'
    ]


# регистрация названия обеспокоенностей
@admin.register(ConcernName)
class ConcernNameAdmin(GuardedModelAdmin):
    """
    Модель отображения названий
    обеспокоенностей в админ панели.
    """
    list_display = [
        'pk',
        'company_name',
        'description'
    ]

    def get_queryset(self, request):
        """
        Метод, фильтрующий названия обеспокоенностей,
        исходя из компании, в которой работает пользователь.
        """

        # Получаем список записей
        queryset = super().get_queryset(request)

        if not request.user.is_superuser:
            queryset = queryset.filter(company_name=request.user.company_name)
        
        return queryset


# Регистрация модели решения обеспокоенностей
@admin.register(ConcernHandle)
class ConcernsHandleAdmin(GuardedModelAdmin):
    list_display = [
        'pk',
        'responsible_user',
        'concern',
        'solution',
    ]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not request.user.is_superuser:
            user_companies = Company.objects.filter(
                customuser__id=request.user.id
            )
            # Фильтруем queryset по полю company_name из модели CustomUser
            queryset = queryset.filter(
                concern__added_by__company_name__in=user_companies
            )

        return queryset
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if not request.user.is_superuser:
            user_companies = Company.objects.filter(customuser__id=request.user.id)
            form.base_fields['responsible_user'].queryset = CustomUser.objects.filter(
                company_name__in=user_companies, role__name="Решатель"
            )

        return form


# Регистрация самих обеспокоенностей
@admin.register(Concerns)
class ConcernsAdmin(GuardedModelAdmin):
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

    def get_queryset(self, request):
        """
        Метод, фильтрующий обеспокоенности по компаниям
        для пользователя.
        """
        queryset = super().get_queryset(request)

        if not request.user.is_superuser:
            # Получаем все компании, связанные с пользователем
            user_companies = Company.objects.filter(customuser__id=request.user.id)
            # Получаем все названия обеспокоенностей, связанные с компаниями пользователя
            concern_names = ConcernName.objects.filter(company_name__in=user_companies)
            # Фильтруем queryset
            queryset = queryset.filter(concern_name__in=concern_names)
        return queryset

    def get_form(self, request, obj=None, **kwargs):
        """
        Метод, который предоставляет выбор для редактирования
        Классификаторов только среди классификаторов определённой компании
        пользователя.
        """
        form = super().get_form(request, obj, **kwargs)
        # выполняется проверка на права пользователя
        if not request.user.is_superuser and request.user.has_perm(
            'handling_concerns.change_concerns'
        ):
            # Получаем все компании, связанные с пользователем
            user_companies = Company.objects.filter(customuser__id=request.user.id)
            # Ограничиваем выбор только классификаторами, связанными с компаниями пользователя
            form.base_fields['concern_name'].queryset = ConcernName.objects.filter(
                company_name__in=user_companies
            )
        return form
