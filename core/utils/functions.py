from aiogram import Bot
from aiogram import exceptions
from aiogram.types import Message

import core.config.config as cfg
import core.config.messages as m
import core.utils.db_manager as db
import core.utils.message_sender as ms
from core.utils import ftp_manager as fm
from core.utils.logger import logger


async def clear_chat(bot: Bot, chat_id: int):
    # select array of message_id from db
    result = db.do_sql_select(db.select_messages_query(chat_id))
    message_ids = []
    for row in result:
        message_ids.append(row[0])
    # delete messages from chat and db
    if message_ids:
        await bot.delete_messages(chat_id=chat_id, message_ids=message_ids)
        db.do_sql_modify(db.delete_messages_by_chat_id_query(chat_id))


async def clear_old_messages(bot: Bot):
    logger.info(f'search old messages')
    result = db.do_sql_select(db.select_old_messages_query())
    if not result:
        logger.info(f'old messages not found')
        return
    message_ids = ''
    for row in result:
        chat_id = int(row[0])
        message_id = int(row[1])
        try:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
        except exceptions.TelegramBadRequest as ex:
            logger.error(f'chat_id = {chat_id}, message_id = {message_id}: {ex}')
        message_ids += str(row[1]) + ','
    logger.info(f'old message ({message_ids}) was deleted from tg')
    message_ids = message_ids[:-1]
    db.do_sql_modify(db.delete_messages_by_message_ids_query(message_ids))
    logger.info(f'old messages ({message_ids}) was deleted from db')


async def check_ftp_files_for_all(bot: Bot):
    logger.info(f'search files on dir')
    files_list = [i for i in fm.get_files_list() if cfg.FTP_FILE_EXTENSION in i]
    if not files_list:
        logger.info(f'files not found')
        return
    text = await create_file_list_message(files_list)
    user_list = db.do_sql_select(db.select_subscribed_users_query())
    user_list_str = []
    for user in user_list:
        user_id_str = user[0]
        user_list_str.append(user_id_str)
        user_id = int(user_id_str)
        try:
            sent_message = await bot.send_message(user_id, text, parse_mode="HTML")
            db.do_sql_modify(db.insert_message_query(sent_message.message_id, sent_message.chat.id))
        except exceptions.TelegramBadRequest as ex:
            logger.error(f'chat_id = {user_id}: {ex}')
    logger.info(f'notification for users ({','.join(user_list_str)}) was send')


async def check_ftp_files_for_one_user(message: Message):
    db.do_sql_modify(db.insert_message_query(message.message_id, message.chat.id))
    logger.info(f'search files on dir')
    files_list = [i for i in fm.get_files_list() if cfg.FTP_FILE_EXTENSION in i]
    text = m.nothing_into_dir_text
    if not files_list:
        logger.info(f'files not found')
        await ms.send_message_answer(message, text)
    else:
        text = await create_file_list_message(files_list)
        await ms.send_message_answer(message, text)


async def create_file_list_message(file_names_list: list[str]) -> str:
    message = '\n🔸'.join(file_names_list)
    message = '🔸' + message
    return m.have_files_text + message


async def send_alert_for_all(bot: Bot, alert_text: str):
    user_list = db.do_sql_select(db.select_all_users_query())
    user_list_str = []
    for user in user_list:
        user_id_str = user[0]
        user_list_str.append(user_id_str)
        user_id = int(user_id_str)
        try:
            sent_message = await bot.send_message(user_id, alert_text, parse_mode="HTML")
            db.do_sql_modify(db.insert_message_query(sent_message.message_id, sent_message.chat.id))
        except exceptions.TelegramBadRequest as ex:
            logger.error(f'chat_id = {user_id}: {ex}')
    logger.info(f'alerts for users ({','.join(user_list_str)}) was send')
