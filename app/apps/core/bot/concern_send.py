from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters.text import Text

import static_text as st

router = Router()


@router.message(Text(text=st.concern_create))
async def creation(message: Message):
    """Создание обеспокоенности"""
    await message.answer(
        st.name_concern
    )
