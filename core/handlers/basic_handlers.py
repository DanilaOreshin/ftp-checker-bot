from aiogram.types import Message

import core.config.messages as m
import core.utils.db_manager as db
from core.utils.message_sender import send_message_answer


# handlers
async def default_handler(message: Message):
    db.do_sql_modify(db.insert_message_query(message.message_id, message.chat.id))
    text = m.default_text
    await send_message_answer(message, text)


async def wrong_user_handler(message: Message):
    db.do_sql_modify(db.insert_message_query(message.message_id, message.chat.id))
    text = m.not_registered_text
    await send_message_answer(message, text)
