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


@router.callback_query(
        SendConcern.choosing_menu_points,
        Text(text=st.finish_approve)
)
async def check_results(callback: CallbackQuery, state: FSMContext):
    """Вызов функции /start."""
    # Здесь возможно выбор надо давать, возможно callback
    data = await state.get_data()

    await callback.answer(
        f'{st.finish_approve}'
    )

    # здесь будет функция для api
    print(data)

    username=callback.from_user.username
    print(f'username - {username}')

    await create_concern(username, data)

    await state.clear()
