from django.contrib import admin
from django.urls import reverse, NoReverseMatch
from django.utils.html import format_html
from .models import (
    Concerns, ConcernName,
    ConcernImportance, ConcernStatus,
    ConcernUrgency, ConcernHandle,
    CustomNotification
)

from notifications.admin import NotificationAdmin

from app.apps.companies.models import Company, Department
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
            user_departments = Department.objects.filter(
                customuser__id=request.user.id
            )
            # Фильтруем queryset по полю company_name из модели CustomUser
            queryset = queryset.filter(
                concern__added_by__company_name__in=user_companies,
                concern__added_by__department_name__in=user_departments
            )

        return queryset
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if not request.user.is_superuser:
            user_companies = Company.objects.filter(customuser__id=request.user.id)
            user_departments = Department.objects.filter(customuser__id=request.user.id)
            form.base_fields['responsible_user'].queryset = CustomUser.objects.filter(
                company_name__in=user_companies,
                role__name="Решатель",
                department_name__in=user_departments
            )
            if request.user.is_sorter():
                allowed_fields = ['responsible_user']

                for field_name, field in form.base_fields.items():
                    if field_name not in allowed_fields:
                        field.disabled = True

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
        if not request.user.is_superuser:
            # Получаем все компании, связанные с пользователем
            user_companies = Company.objects.filter(customuser__id=request.user.id)
            # Ограничиваем выбор только классификаторами, связанными с компаниями пользователя
            form.base_fields['concern_name'].queryset = ConcernName.objects.filter(
                company_name__in=user_companies
            )

        return form


admin.site.unregister(CustomNotification)


@admin.register(CustomNotification)
class CustomNotificationAdmin(GuardedModelAdmin):
    raw_id_fields = ('recipient',)
    list_display = ('custom_recipient', 'custom_actor',
                    'custom_target_object_url', 'custom_unread',)

    @admin.display(description="Получатель")
    def custom_recipient(self, obj):
        return obj.recipient
    
    @admin.display(description="Отправитель")
    def custom_actor(self, obj):
        return obj.actor
    
    @admin.display(description="Назначить исполнителя")
    def custom_target_object_url(self, obj):
        try:
            url = reverse("admin:{0}_{1}_change".format(obj.target_content_type.app_label, obj.target_content_type.model), args=(obj.target_object_id,))
            return format_html("<a href='{url}'>{id}</a>", url=url, id=obj.target_object_id)
        except NoReverseMatch:
            return obj.target_object_id
    
    @admin.display(description="Непрочитано")
    def custom_unread(self, obj):
        if obj.unread:
            return format_html('<span style="color:green;">&#x2713;</span>')
        else:
            return format_html('<span style="color:red;">&#x2717;</span>')

    fieldsets = (
        ('Общая инофрмация', {'fields': (
            'actor_object_id',
            'recipient',
            'target_object_id',
            'verb',
            'unread',
        )}),
    )
