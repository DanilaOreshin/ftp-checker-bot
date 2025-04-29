from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram.types import Message

import core.config.messages as m
import core.keyboards.keyboard_builder as kb
import core.utils.db_manager as db
import core.utils.functions as func
import core.utils.message_sender as ms
from core.filters.check_user import is_registered
from core.keyboards.button import Button


# handlers
async def start_command_handler(message: Message):
    user_id = message.from_user.id
    db.do_sql_modify(db.insert_message_query(message.message_id, user_id))
    if not is_registered(user_id):
        text = m.start_registration_text
        reply_builder = kb.get_inline_keyboard([Button(text='✍️Регистрация', callback_data='register')])
        await ms.send_message_answer_with_buttons(message, text, reply_builder.as_markup())
    else:
        text = m.welcome_text
        reply_builder = kb.get_reply_keyboard([Button(text='🔍Проверить сейчас'), Button(text='⚙️Управление подпиской')])
        await message.answer(text, parse_mode="HTML", reply_markup=reply_builder.as_markup(resize_keyboard=True))


async def about_command_handler(message: Message):
    db.do_sql_modify(db.insert_message_query(message.message_id, message.chat.id))
    text = m.about_text
    await ms.send_message_answer(message, text)


async def send_alert_command_handler(message: Message, command: CommandObject, bot: Bot):
    db.do_sql_modify(db.insert_message_query(message.message_id, message.chat.id))
    alert_text = command.args
    await func.send_alert_for_all(bot, alert_text)
    text = "Done!"
    await ms.send_message_answer(message, text)
