from typing import Optional

from aiogram import Bot, exceptions
from aiogram.types import Message, CallbackQuery, ReplyMarkupUnion

from src.config.bot_config import config as cfg
from src.services import db_manager as db
from src.utils.logger import logger


async def send_call_answer(call: CallbackQuery, text: str, markup: Optional[ReplyMarkupUnion] = None):
    sent_message = await call.message.answer(text=text, reply_markup=markup)
    await db.save_message(sent_message)
    await call.answer()


async def send_message_answer(message: Message, text: str, markup: Optional[ReplyMarkupUnion] = None):
    sent_message = await message.answer(text, reply_markup=markup)
    await db.save_message(sent_message)


async def delete_message_from_tg(bot: Bot, chat_id: int, message_id: int):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except exceptions.TelegramBadRequest as ex:
        logger.error(f'chat_id = {chat_id}, message_id = {message_id}: {ex}')


async def clear_target_chat(bot: Bot, chat_id: int):
    message_list = [item[0] for item in await db.sql_select(db.select_messages_query(chat_id))]
    if message_list:
        for message_id in message_list:
            await delete_message_from_tg(bot, chat_id, message_id)
        await db.sql_modify(db.delete_messages_by_message_ids_query(message_list))


async def clear_old_messages(bot: Bot):
    result = await db.sql_select(db.select_old_messages_query(cfg.INTERVAL_OLD_MSG_PERIOD))
    if not result:
        return
    message_list = []
    for chat_id, message_id in result:
        await delete_message_from_tg(bot, chat_id, message_id)
        message_list.append(message_id)
    await db.sql_modify(db.delete_messages_by_message_ids_query(message_list))
