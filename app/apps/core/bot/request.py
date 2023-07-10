from django.utils import timezone
from asgiref.sync import sync_to_async

from app.apps.handling_concerns.models import (Concerns,
                                               ConcernName,
                                               ConcernUrgency,
                                               ConcernImportance)

from app.apps.users.models import CustomUser


@sync_to_async
def create_concern(username: str, data: dict):
    # Получите или создайте экземпляр связанных моделей
    concern_name = ConcernName.objects.get_or_create(
        description=data.get('concern_name', "")
    )[0]
    concern_urgency = ConcernUrgency.objects.get_or_create(
        description=data.get('concern_urgency', "")
    )[0]
    concern_importance = ConcernImportance.objects.get_or_create(
        description=data.get('concern_importance', "")
    )[0]

    # Создайте экземпляр Concerns и установите значения полей
    concern = Concerns()
    concern.added_by = CustomUser.objects.get(username=username)
    concern.concern_name = concern_name
    concern.concern_urgency = concern_urgency
    concern.concern_importance = concern_importance
    concern.concern_title = data.get('concern_title', "")
    concern.concern_description = data.get('concern_description', "")
    concern.concern_effect = data.get('concern_effect', "")
    concern.concern_reason = data.get('concern_reason', "")
    concern.concern_solution = data.get('concern_solution', "")
    concern.added = timezone.now()

    # Сохраните экземпляр
    concern.save()
