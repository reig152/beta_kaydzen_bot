import requests

from app.apps.users.models import CustomUser

from app.apps.core.models import TGUser
from app.config.bot import TG_TOKEN as token


def send_telegram(instance, **kwargs):
    # определим текст уведомления
    text = (f"Создана {instance.concern_importance} обеспокоенность:"
            f"{instance.concern_description[:20]}")
    # найдем chat id пользователя
    # Получаем всех сортировщиков департамента пользователя
    author_department = instance.added_by.department_name

    # Получаем всех сортировщиков
    sorters = CustomUser.objects.filter(
        role__name='Сортировщик',
        department_name=author_department
    )

    # отправка сообщения
    url = f'https://api.telegram.org/bot{token}/sendMessage'

    for chat in sorters:
        try:
            chat_id = TGUser.objects.get(
                username__username=chat.username
            )

            data = {'chat_id': chat_id.chat_id,
                    'text': text
                    }
            response = requests.post(url=url, data=data)
            print(response)

        except Exception as ex:
            print(f'Возникла ошибка уведомления: {ex}')
