from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram.types import Message

import src.config.messages as m
import src.keyboards.keyboard_builder as kb
import src.utils.db_manager as db
import src.utils.functions as func
import src.utils.message_sender as ms
from src.filters.check_user import is_registered
from src.keyboards.button import Button


# handlers
async def start_command_handler(message: Message):
    await db.save_message(message)
    if not await is_registered(message.from_user.id):
        text = m.start_registration_text
        reply_builder = kb.get_inline_keyboard([Button(text='✍️Регистрация', callback_data='register')])
        await ms.send_message_answer_with_buttons(message, text, reply_builder.as_markup())
    else:
        text = m.welcome_text
        reply_builder = kb.get_reply_keyboard([Button(text='🔍Проверить сейчас'), Button(text='⚙️Управление подпиской')])
        await message.answer(text, reply_markup=reply_builder.as_markup(resize_keyboard=True))


async def about_command_handler(message: Message):
    await db.save_message(message)
    text = m.about_text
    await ms.send_message_answer(message, text)


async def send_alert_command_handler(message: Message, command: CommandObject, bot: Bot):
    await db.save_message(message)
    alert_text = command.args
    await func.send_alert_for_all(bot, alert_text)
    text = "Done!"
    await ms.send_message_answer(message, text)
