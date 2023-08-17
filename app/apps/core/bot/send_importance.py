from asyncio import to_thread

from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

import app.apps.core.bot.keyboards as kb
import app.apps.core.bot.static_text as st

from .handlers import SendConcern
from .keyboards import finish_kb, make_filters_kb


router = Router()


@router.callback_query(
        SendConcern.choosing_menu_points,
        Text(text=st.type_importance)
)
async def choose_menu_points(
        callback: CallbackQuery,
        state: FSMContext):
    """Выбор пунктов меню."""
    importance_type = 'description'
    importance_model = 'ConcernImportance'
    reply_markup = await to_thread(make_filters_kb, importance_model, importance_type)
    await callback.message.edit_text(
        text=st.concern_importance_text,
        reply_markup=reply_markup
    )

    await state.set_state(SendConcern.at_importance)


@router.callback_query(
        SendConcern.at_importance,
        Text(text=st.finish_approve)
)
async def edit_choice(
        callback: CallbackQuery,
        state: FSMContext):
    await callback.message.edit_text(
        text=st.menu_points,
        reply_markup=kb.main_menu_kb()
    )

    await state.set_state(SendConcern.choosing_menu_points)


@router.callback_query(
        SendConcern.at_importance,
        Text(text=st.edit_choice_text)
)
async def choose_menu_points(
        callback: CallbackQuery,
        state: FSMContext):
    """Выбор пунктов меню."""
    importance_type = 'description'
    importance_model = 'ConcernImportance'
    reply_markup = await to_thread(make_filters_kb, importance_model, importance_type)
    await callback.message.edit_text(
        text=st.concern_importance_text,
        reply_markup=reply_markup
    )

    await state.set_state(SendConcern.at_importance)


@router.callback_query(
    SendConcern.at_importance,
)
async def importance_chosen(
        callback: CallbackQuery,
        state: FSMContext):
    """Обрабротка выбранной срочности."""

    await state.update_data(concern_importance=callback.data)

    chosen_importance = await state.get_data()

    await callback.message.edit_text(
        text=f"{st.choice_text} {chosen_importance.get('concern_importance', '')}",
        reply_markup=kb.check_data_kb()
    )
