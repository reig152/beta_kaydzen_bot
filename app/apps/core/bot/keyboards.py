from aiogram.types import (ReplyKeyboardMarkup,
                           InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

import app.apps.core.bot.static_text as st

from .get_attributes import get_all_attributes


def start_menu_kb() -> InlineKeyboardButton:
    """Клавиатура начала работы бота."""
    kb = InlineKeyboardBuilder()
    kb.button(text=st.concern_create,
              callback_data=st.concern_create)
    kb.adjust(1)

    return kb.as_markup(resize_keyboard=True)


def main_menu_kb() -> InlineKeyboardButton:
    """Клавиатура главного меню."""
    kb = InlineKeyboardBuilder()
    kb.button(text=st.type_classificator,
              callback_data=st.type_classificator)
    kb.button(text=st.type_urgency,
              callback_data=st.type_urgency)
    kb.button(text=st.type_importance,
              callback_data=st.type_importance)
    kb.button(text=st.type_naming,
              callback_data=st.type_naming)
    kb.button(text=st.type_description,
              callback_data=st.type_description)
    kb.button(text=st.type_effect,
              callback_data=st.type_effect)
    kb.button(text=st.type_reason,
              callback_data=st.type_reason)
    kb.button(text=st.type_reason,
              callback_data=st.type_reason)
    kb.button(text=st.finish_approve,
              callback_data=st.finish_approve)
    
    kb.adjust(2)

    return kb.as_markup(resize_keyboard=True)


def finish_kb() -> ReplyKeyboardMarkup:
    """Клавиатура отправки обеспокоенности."""
    kb = ReplyKeyboardBuilder()
    kb.button(text=st.concern_create)
    kb.adjust(1)

    return kb.as_markup(resize_keyboard=True)


def make_filters_kb(urgency_model, attr: str) -> InlineKeyboardButton:
    """Функция конструктор клавитаур."""
    kb = InlineKeyboardBuilder()
    filters = get_all_attributes(urgency_model, attr)
    for param in filters:
        if param is not None:
            kb.button(text=param,
                      callback_data=param)

    kb.adjust(1)

    return kb.as_markup(resize_keyboard=True)


def check_data_kb() -> InlineKeyboardButton:
    """Клавиатура проверки выбора."""
    kb = InlineKeyboardBuilder()
    kb.button(text=st.finish_approve,
              callback_data=st.finish_approve)
    kb.button(text=st.edit_choice_text,
              callback_data=st.edit_choice_text)
    kb.adjust(2)

    return kb.as_markup(resize_keyboard=True)
