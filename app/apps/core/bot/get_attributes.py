from app.apps.handling_concerns.models import ConcernUrgency


def get_all_attributes(attr):
    """Функция собирает наименования кнопок для клавиатуры."""
    all_attr = []
    attrib = list(
        ConcernUrgency.objects.values_list(attr, flat=True).distinct()
    )
    for x in attrib:
        if x not in all_attr:
            all_attr.append(x)
    return all_attr
