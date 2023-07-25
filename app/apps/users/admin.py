from django.contrib import admin
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

import django.contrib.auth.admin
import django.contrib.auth.models
from django.contrib import auth

from .models import CustomUser, Role, CustomPermission
from app.apps.companies.models import Company



@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    filter_horizontal = ('permissions',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if 'permissions' in form.base_fields:
            excluded_content_types = ContentType.objects.filter(model__in=[
                'logentry', 'group', 'user',
                'session', 'permission', 'contenttype',
                'userobjectpermission',
                'groupobjectpermission',
                'custompermission',
            ])
            form.base_fields['permissions'].queryset = CustomPermission.objects.exclude(
                content_type__in=excluded_content_types
            )

        return form


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Модель отображения полей в админ панели."""

    list_display = [
        'pk',
        'username',
        'telegram_username',
        'role',
        'company_name',
    ]

    # Фильтрация по ролям
    list_filter = [
        'company_name',
        'role',
    ]

    # Поиск по username
    search_fields = [
        'username',
    ]

    # настраиваем форму создания пользователя
    fieldsets = (
        ('Логин и пароль', {'fields': ('username', 'password')}),
        ('Личная информация', {'fields': (
            'first_name',
            'last_name',
            'middle_name',
            'email',
            'mobile',
            'telegram_username',
            'company_name',
            'position'
        )}),
        ('Права доступа', {'fields': (
            'is_staff',
            'is_superuser',
            'role',
        )}),
    )

    def get_queryset(self, request):
        """
        Метод, фильтрующий пользователей по компаниям.
        """
        queryset = super().get_queryset(request)

        if not request.user.is_superuser:
            # Получаем все компании, связанные с пользователем
            user_companies = Company.objects.filter(customuser__id=request.user.id)
            queryset = queryset.filter(company_name__in=user_companies)
        return queryset

    def get_form(self, request, obj=None, **kwargs):
        """
        Метод, который предоставляет выбор для редактирования
        компаний сотрудников.
        """
        form = super().get_form(request, obj, **kwargs)
        # выполняется проверка на права пользователя
        if not request.user.is_superuser and request.user.has_perms(
            ['users.change_customuser', 'users.add_customuser']
        ):
            # Ограничиваем выбор только классификаторами, связанными с компаниями пользователя
            form.base_fields['company_name'].queryset = Company.objects.filter(
                customuser__id=request.user.id
            )
            form.base_fields['is_superuser'].disabled = True

        if not request.user.is_superuser and obj == request.user:
            form.base_fields['role'].disabled = True
            form.base_fields['is_staff'].disabled = True
            form.base_fields['company_name'].disabled = True

        return form

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Проверяем, является ли объект новым (еще не сохраненным в базе)
            obj.set_password(form.cleaned_data['password'])  # Хешируем пароль
        super().save_model(request, obj, form, change)


admin.site.unregister(auth.models.Group)
