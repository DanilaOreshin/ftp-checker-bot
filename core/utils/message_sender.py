from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardMarkup

import core.utils.db_manager as db


async def send_call_answer(call: CallbackQuery, text: str):
    sent_message = await call.message.answer(text, parse_mode="HTML")
    db.do_sql_modify(db.insert_message_query(sent_message.message_id, sent_message.chat.id))
    await call.answer()


async def send_message_answer(message: Message, text: str):
    sent_message = await message.answer(text, parse_mode="HTML")
    db.do_sql_modify(db.insert_message_query(sent_message.message_id, sent_message.chat.id))


async def send_call_answer_with_buttons(call: CallbackQuery, text: str, markup: InlineKeyboardMarkup):
    sent_message = await call.message.answer(text, parse_mode="HTML", reply_markup=markup)
    db.do_sql_modify(db.insert_message_query(sent_message.message_id, sent_message.chat.id))
    await call.answer()


async def send_message_answer_with_buttons(message: Message, text: str, markup):
    sent_message = await message.answer(text, parse_mode="HTML", reply_markup=markup)
    db.do_sql_modify(db.insert_message_query(sent_message.message_id, sent_message.chat.id))
