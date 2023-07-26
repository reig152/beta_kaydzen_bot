from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import ConcernImportance, ConcernStatus


@receiver(post_migrate)
def create_default_statuses(sender, **kwargs):
    if sender.name == 'app.apps.handling_concerns':
        ConcernStatus.objects.get_or_create(
            description='B процессе'
        )
        ConcernStatus.objects.get_or_create(
            description='Завершено'
        )
        ConcernImportance.objects.get_or_create(
            description='Аварийная'
        )
        ConcernImportance.objects.get_or_create(
            description='Обычная'
        )


# if sender.name == 'your_app_name':  # Замените на имя вашего приложения
#         # Список дефолтных объектов для модели ConcernTypes
#         default_concern_types = [
#             {'description': 'Default Type 1'},
#             {'description': 'Default Type 2'},
#             # Добавьте другие дефолтные объекты, если требуется
#         ]
        
#         # Используем bulk_create() для создания нескольких объектов одним запросом к базе данных
#         ConcernTypes.objects.bulk_create([
#             ConcernTypes.objects.get_or_create(**data)[0] for data in default_concern_types
#         ])