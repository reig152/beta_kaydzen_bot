from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Role, CustomPermission


@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    # Проверяем, что сигнал был отправлен после создания таблиц для приложения вашего проекта
    if sender.name == 'app.apps.users':
        # Определяем дефолтные роли, которые
        # будут созданы после произведения миграций
        default_roles = [
            {
                'name': 'Решатель',
                'permissions': [
                    # перечисляем права для решателя
                    # по аналогии сделаем с другими дефолтными ролями
                    'add_concerns', 
                    'change_concerns',
                    'view_concerns',
                    'change_concernhandle',
                    'delete_concernhandle',
                    'view_concernhandle',
                ]
            },
            {
                'name': 'Админ-клиент',
                'permissions': [
                    # Здесь перечислите коды прав для роли 2
                    'add_concernimportance',
                    'change_concernimportance',
                    'delete_concernimportance',
                    'view_concernimportance',
                    'add_concernname',
                    'change_concernname',
                    'delete_concernname',
                    'view_concernname',
                    'add_concerns',
                    'change_concerns',
                    'delete_concerns',
                    'view_concerns',
                    'change_concernstatus',
                    'delete_concernstatus',
                    'view_concernstatus',
                    'add_concernurgency',
                    'change_concernurgency',
                    'delete_concernurgency',
                    'view_concernurgency',
                    'view_custompermission',
                    'add_role',
                    'change_role',
                    'delete_role',
                    'view_role',
                    'view_tguser',
                    'add_customuser',
                    'change_customuser',
                    'delete_customuser',
                    'view_customuser',
                    'change_concernhandle',
                    'add_concernhandle',
                    'delete_concernhandle',
                    'view_concernhandle',
                ]
            },
            {
                'name': 'Отправитель',
                'permissions': [
                    # Здесь перечислите коды прав для роли 2
                    'add_concerns',
                ]
            },
            {
                'name': 'Сортировщик',
                'permissions': [
                    # Здесь перечислите коды прав для роли 2
                    'change_concerns',
                    'view_concerns',
                ]
            },
        ]

        for role_data in default_roles:
            role_name = role_data['name']
            permissions = role_data['permissions']

            role, _ = Role.objects.get_or_create(name=role_name)

            # Добавляем права к роли
            for permission_code in permissions:
                try:
                    permission = CustomPermission.objects.get(codename=permission_code)
                    role.permissions.add(permission)
                except CustomPermission.DoesNotExist:
                    # Обработка случая, когда указано несуществующее право
                    pass

            # Сохраняем роль
            role.save()
