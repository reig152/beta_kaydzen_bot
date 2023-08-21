from asyncio import to_thread

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.filters.text import Text
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.apps.core.bot.static_text as st
import app.apps.core.bot.keyboards as kb

from app.apps.core.use_case import CORE_USE_CASE
from app.config.application import INSTALLED_APPS

from .get_attributes import get_status


router = Router()


class SendConcern(StatesGroup):
    """Машина состояний отправки обеспокоенностей."""
    at_main_menu = State()
    choosing_menu_points = State()
    at_classificator = State()
    at_urgency = State()
    at_importance = State()
    at_naming = State()
    at_describing = State()
    at_economics_effect = State()
    at_reason = State()
    at_solution = State()
    at_finish = State()


@router.message(Command(commands=["start"]))
async def handle_start_command(message: Message, state: FSMContext) -> None:
    await state.clear()

    if message.from_user is None:
        return

    tg_user = await CORE_USE_CASE.register_bot_user(
        user_id=message.from_user.id,
        chat_id=message.chat.id,
        username=message.from_user.username,
    )

    if tg_user is None:
        await message.answer("You don't have perms to the bot!")
    else:
        await message.answer(
            "You have successfully registered in the bot!",
            reply_markup=kb.start_menu_kb()
        )
        await state.set_state(SendConcern.at_main_menu)


@router.message(Command(commands=["statuses"]))
async def get_concern_status(message: Message, state: FSMContext):
    await state.clear()

    # необходимо получить статус и отправить его пользователю
    username = message.from_user.username

    msg_list = await to_thread(get_status, username)

    for msg in msg_list:
        if msg_list:
            await message.answer(
                msg,
                parse_mode="HTML"
            )
        else:
            await message.answer(
                "У вас нет зарегистированных обеспокоенностей",
                parse_mode="HTML"
            )


# добавить хендлер с кнопкой главного меню
#
@router.callback_query(
        SendConcern.at_main_menu,
        Text(st.concern_create)
)
async def cmd_start(callback: CallbackQuery, state: FSMContext):
    """Вызов функции /start."""
    await callback.message.edit_text(
        st.menu_points,
        reply_markup=kb.main_menu_kb()
    )

    await state.set_state(SendConcern.choosing_menu_points)
 

@router.message(Command(commands=["apps"]))
async def handle_apps_command(message: Message) -> None:
    apps_names = [app_name for app_name in INSTALLED_APPS if app_name.startswith("app.")]
    await message.answer("Installed apps:\n" f"{apps_names}")


@router.message(Command(commands=["id"]))
async def handle_id_command(message: Message) -> None:
    if message.from_user is None:
        return

    await message.answer(
        f"User Id: <b>{message.from_user.id}</b>\n" f"Chat Id: <b>{message.chat.id}</b>"
    )
