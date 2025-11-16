from aiogram import Bot, exceptions
from aiogram.filters import CommandObject
from aiogram.types import Message

import src.texts.messages_texts as m
import src.services.db_manager as db
from src.utils.components import welcome_message_component, start_registration_component
from src.utils.functions import is_registered
from src.services.message_manager import send_message_answer
from src.utils.logger import logger


async def start_command_handler(message: Message):
    if await is_registered(message.from_user.id):
        text, builder = welcome_message_component()
        await message.answer(text, reply_markup=builder.as_markup(resize_keyboard=True))
    else:
        text, builder = start_registration_component()
        await send_message_answer(message, text, builder.as_markup())


async def about_command_handler(message: Message):
    text = m.ABOUT_COMMAND
    await send_message_answer(message, text)


async def help_command_handler(message: Message):
    text = m.HELP_COMMAND
    await send_message_answer(message, text)


async def alert_command_handler(message: Message, command: CommandObject, bot: Bot):
    alert_text = command.args
    user_list = [user[0] for user in await db.sql_select(db.select_all_users_query())]
    for user_id in user_list:
        try:
            sent_message = await bot.send_message(user_id, alert_text)
            await db.save_message(sent_message)
        except exceptions.TelegramBadRequest as ex:
            logger.error(f'user_id = {user_id}: {ex}')
    text = m.ALERT_SENT
    await send_message_answer(message, text)
