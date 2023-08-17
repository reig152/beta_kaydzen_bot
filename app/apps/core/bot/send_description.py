from asyncio import to_thread

from aiogram import Router
from aiogram.filters.text import Text
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

import app.apps.core.bot.keyboards as kb
import app.apps.core.bot.static_text as st

from .handlers import SendConcern
from .keyboards import finish_kb, make_filters_kb


router = Router()


@router.callback_query(
        SendConcern.choosing_menu_points,
        Text(text=st.type_description)
)
async def choose_menu_points(
        callback: CallbackQuery,
        state: FSMContext):
    """Выбор пунктов меню."""

    await callback.message.edit_text(
        text=st.concern_description_text,
    )

    await state.set_state(SendConcern.at_describing)


@router.callback_query(
        SendConcern.at_describing,
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
        SendConcern.at_describing,
        Text(text=st.edit_choice_text)
)
async def choose_menu_points(
        callback: CallbackQuery,
        state: FSMContext):
    """Выбор пунктов меню."""

    await callback.message.edit_text(
        text=st.concern_description_text,
    )

    await state.set_state(SendConcern.at_describing)


@router.message(
    SendConcern.at_describing,
)
async def classificator_chosen(
        message: Message,
        state: FSMContext):
    """Обрабротка выбранной срочности."""

    await state.update_data(concern_description=message.text)

    chosen_description = await state.get_data()

    await message.answer(
        text=f"{st.choice_text} {chosen_description.get('concern_description', '')}",
        reply_markup=kb.check_data_kb()
    )
