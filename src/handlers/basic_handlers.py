from aiogram.types import Message

import src.texts.messages_texts as m
from src.services.message_manager import send_message_answer


async def default_handler(message: Message):
    text = m.DEFAULT
    await send_message_answer(message, text)


async def wrong_user_handler(message: Message):
    text = m.UNREGISTERED
    await send_message_answer(message, text)
