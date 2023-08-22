from app.apps.handling_concerns.models import Concerns
from django.apps import apps



def get_all_attributes(model_name, attr):
    """Функция собирает наименования кнопок для клавиатуры."""
    ModelClass = apps.get_model('handling_concerns', model_name)
    all_attr = []
    attrib = list(
        ModelClass.objects.values_list(attr, flat=True).distinct()
    )
    for x in attrib:
        if x not in all_attr:
            all_attr.append(x)
    return all_attr


def get_status(username):
    """Функция получает последние 10 обеспокоенностей пользователя."""
    # получаем обеспокоенности пользователя
    concerns = Concerns.objects.filter(
        added_by__username=username
    )[:10]
    msg_list = []
    for concern in concerns:
        try:
        # составим текст сообщения
            text = (
                f"Id обеспокоенности: {concern.pk}\n"
                f"Наименование обеспокоенности: {concern.concern_name}\n"
                f"Статус обеспокоенности: {concern.concern_status}\n"
            )
            msg_list.append(text)

        except Exception:
            text = "У вас нет зарегистированных обеспокоенностей"
            msg_list.append(text)
            print(Exception)

    return msg_list
