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
        Text(text=st.type_classificator)
)
async def choose_menu_points(
        callback: CallbackQuery,
        state: FSMContext):
    """Выбор пунктов меню."""
    classificator_type = 'description'
    classificator_model = 'ConcernName'
    reply_markup = await to_thread(
        make_filters_kb,
        classificator_model,
        classificator_type
    )
    await callback.message.edit_text(
        text=st.name_concern,
        reply_markup=reply_markup
    )

    await state.set_state(SendConcern.at_classificator)


@router.callback_query(
        SendConcern.at_classificator,
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
        SendConcern.at_classificator,
        Text(text=st.edit_choice_text)
)
async def choose_menu_points(
        callback: CallbackQuery,
        state: FSMContext):
    """Выбор пунктов меню."""
    classificator_type = 'description'
    classificator_model = 'ConcernName'
    reply_markup = await to_thread(
        make_filters_kb,
        classificator_model,
        classificator_type
    )
    await callback.message.edit_text(
        text=st.name_concern,
        reply_markup=reply_markup
    )

    await state.set_state(SendConcern.at_classificator)


@router.callback_query(
    SendConcern.at_classificator,
)
async def classificator_chosen(
        callback: CallbackQuery,
        state: FSMContext):
    """Обрабротка выбранной срочности."""

    await state.update_data(concern_classificator=callback.data)

    chosen_classificator = await state.get_data()

    await callback.message.edit_text(
        text=f"{st.choice_text} {chosen_classificator.get('concern_classificator', '')}",
        reply_markup=kb.check_data_kb()
    )
