# В файле urls.py вашего приложения
from django.urls import path
from .views import register_users_from_excel

app_name = 'for_admin'  # Замените 'your_app_name' на имя вашего приложения

urlpatterns = [
    # Другие URL-шаблоны вашего приложения
    path('register_users_from_excel/', register_users_from_excel, name='register_users_from_excel'),
]
