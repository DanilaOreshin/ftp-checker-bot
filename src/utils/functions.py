from aiogram import Bot
from aiogram import exceptions
from aiogram.types import Message

import src.config.messages as m
import src.utils.db_manager as db
import src.utils.ftp_manager as fm
import src.utils.message_sender as ms
from src.config.bot_settings import settings as cfg
from src.utils.logger import logger


async def clear_chat(bot: Bot, chat_id: int):
    # select array of message_id from db
    result = await db.sql_select(db.select_messages_query(chat_id))
    message_ids = []
    for row in result:
        message_ids.append(row[0])
    # delete messages from chat and db
    if message_ids:
        await bot.delete_messages(chat_id=chat_id, message_ids=message_ids)
        await db.sql_modify(db.delete_messages_by_chat_id_query(chat_id))


async def clear_old_messages(bot: Bot):
    logger.info(f'search old messages')
    result = await db.sql_select(db.select_old_messages_query(cfg.INTERVAL_OLD_MSG_PERIOD))
    if not result:
        logger.info(f'old messages not found')
        return
    message_ids = list()
    for row in result:
        chat_id = row[0]
        message_id = row[1]
        try:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
            logger.info(f'old message message_id was deleted from tg')
        except exceptions.TelegramBadRequest as ex:
            logger.error(f'chat_id = {chat_id}, message_id = {message_id}: {ex}')
        message_ids.append(row[1])
    await db.sql_modify(db.delete_messages_by_message_ids_query(message_ids))
    logger.info(f'old messages ({message_ids}) was deleted from db')


async def check_ftp_files_for_all(bot: Bot):
    logger.info(f'search files on dir')
    files_list = [i for i in fm.get_files_list() if cfg.FTP_FILE_EXTENSION in i]
    if not files_list:
        logger.info(f'files not found')
        return
    text = await create_file_list_message(files_list)
    user_list = await db.sql_select(db.select_subscribed_users_query())
    user_list_str = []
    for user in user_list:
        user_id = user[0]
        try:
            sent_message = await bot.send_message(user_id, text)
            await db.save_message(sent_message)
        except exceptions.TelegramBadRequest as ex:
            logger.error(f'chat_id = {user_id}: {ex}')
        user_list_str.append(str(user_id))
    logger.info(f'notification for users ({','.join(user_list_str)}) was send')


async def check_ftp_files_for_one_user(message: Message):
    await db.save_message(message)
    logger.info(f'search files on dir')
    raw_files = fm.get_files_list()
    expected_files = [i for i in raw_files if cfg.FTP_FILE_EXTENSION in i]
    text = m.nothing_into_dir_text
    if not expected_files:
        logger.info(f'files not found')
        await ms.send_message_answer(message, text)
    else:
        text = await create_file_list_message(expected_files)
        await ms.send_message_answer(message, text)


async def create_file_list_message(file_names_list: list[str]) -> str:
    message = '\n🔸'.join(file_names_list)
    message = '🔸' + message
    return m.have_files_text + message


async def send_alert_for_all(bot: Bot, alert_text: str):
    user_list = await db.sql_select(db.select_all_users_query())
    user_list_str = []
    for user in user_list:
        user_id = user[0]
        try:
            sent_message = await bot.send_message(user_id, alert_text)
            await db.save_message(sent_message)
        except exceptions.TelegramBadRequest as ex:
            logger.error(f'chat_id = {user_id}: {ex}')
        user_list_str.append(str(user_id))
    logger.info(f'alerts for users ({','.join(user_list_str)}) was send')
