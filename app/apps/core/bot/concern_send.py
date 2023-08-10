from asyncio import to_thread

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters.text import Text
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.apps.core.bot.static_text as st

from .handlers import SendConcern
from .keyboards import finish_kb, make_filters_kb

from .request import create_concern


router = Router()


@router.message(
        SendConcern.at_classificator
)
async def typing_classificator(message: Message, state: FSMContext):
    """Вызов функции /start."""
    urgency_type = 'description'
    urgency_model = 'ConcernUrgency'
    reply_markup = await to_thread(make_filters_kb, urgency_model, urgency_type)

    await message.answer(
        st.concern_urgency_text,
        reply_markup=reply_markup
    )

    await state.update_data(concern_name=message.text)

    await state.set_state(SendConcern.at_urgency)


@router.callback_query(
        SendConcern.at_urgency,
)
async def typing_urgency(callback: CallbackQuery, state: FSMContext):
    urgency_type = 'description'
    urgency_model = 'ConcernImportance'
    reply_markup = await to_thread(make_filters_kb, urgency_model, urgency_type)

    await callback.message.edit_text(
        st.concern_importance_text,
        reply_markup=reply_markup
    )

    await state.update_data(concern_urgency=callback.data)

    await state.set_state(SendConcern.at_importance)


@router.callback_query(
        SendConcern.at_importance,
)
async def typing_importance(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_text(
        st.concern_naming_text
    )

    await state.update_data(concern_importance=callback.data)

    await state.set_state(SendConcern.at_naming)


@router.message(
        SendConcern.at_naming,
)
async def typing_naming(message: Message, state: FSMContext):

    await message.answer(
        st.concern_description_text
    )

    await state.update_data(concern_title=message.text)

    await state.set_state(SendConcern.at_describing)


@router.message(
        SendConcern.at_describing,
)
async def typing_description(message: Message, state: FSMContext):

    await message.answer(
        st.concern_economics_effect
    )

    await state.update_data(concern_description=message.text)

    await state.set_state(SendConcern.at_economics_effect)


@router.message(
        SendConcern.at_economics_effect,
)
async def typing_economics_effects(message: Message, state: FSMContext):

    await message.answer(
        st.concern_reason_text
    )

    await state.update_data(concern_effect=message.text)

    await state.set_state(SendConcern.at_reason)


@router.message(
        SendConcern.at_reason,
)
async def typing_reason(message: Message, state: FSMContext):

    await message.answer(
        st.concern_solution_text
    )

    await state.update_data(concern_reason=message.text)

    await state.set_state(SendConcern.at_solution)


@router.message(
        SendConcern.at_solution,
)
async def typing_solution(message: Message, state: FSMContext):

    await state.update_data(concern_solution=message.text)

    data = await state.get_data()

    await message.answer(
        f'{st.finish_text} \n'
        f'{data.get("concern_name", "")} \n'
        f'{data.get("concern_urgency", "")} \n'
        f'{data.get("concern_importance", "")} \n'
        f'{data.get("concern_title", "")} \n'
        f'{data.get("concern_description", "")} \n'
        f'{data.get("concern_effect", "")} \n'
        f'{data.get("concern_reason", "")} \n'
        f'{data.get("concern_solution", "")}',
        reply_markup=finish_kb()
    )

    await state.set_state(SendConcern.at_finish)


@router.message(
        SendConcern.at_finish,
)
async def check_results(message: Message, state: FSMContext):
    """Вызов функции /start."""
    # Здесь возможно выбор надо давать, возможно callback
    data = await state.get_data()

    await message.answer(
        f'{st.finish_approve}'
    )

    # здесь будет функция для api
    print(data)

    username=message.from_user.username

    await create_concern(username, data)

    await state.clear()
