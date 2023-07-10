from aiogram.types import (ReplyKeyboardMarkup,
                           InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

import app.apps.core.bot.static_text as st

from .get_attributes import get_all_attributes


def start_menu_kb() -> InlineKeyboardButton:
    """Клавиатура создания обеспокоенности."""
    kb = InlineKeyboardBuilder()
    kb.button(text=st.concern_create,
              callback_data=st.concern_create)
    kb.adjust(1)

    return kb.as_markup(resize_keyboard=True)


def finish_kb() -> ReplyKeyboardMarkup:
    """Клавиатура создания обеспокоенности."""
    kb = ReplyKeyboardBuilder()
    kb.button(text=st.concern_create)
    kb.adjust(1)

    return kb.as_markup(resize_keyboard=True)


def make_filters_kb(attr: str) -> InlineKeyboardButton:
    """Функция конструктор клавитаур."""
    attributes = attr
    kb = InlineKeyboardBuilder()
    filters = get_all_attributes(attributes)
    for param in filters:
        if param is not None:
            kb.button(text=param,
                      callback_data=param)

    kb.adjust(1)

    return kb.as_markup(resize_keyboard=True)