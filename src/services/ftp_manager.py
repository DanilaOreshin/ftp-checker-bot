from ftplib import FTP

from aiogram import Bot, exceptions

from src.config.bot_config import config as cfg
from src.services import db_manager as db
from src.texts import messages_texts as m
from src.utils.logger import logger


def ftp_connect() -> FTP():
    ftp = FTP()
    try:
        ftp.connect(host=cfg.FTP_HOST, port=cfg.FTP_PORT, timeout=30)
        ftp.login(user=cfg.FTP_USER, passwd=cfg.FTP_PASSWORD)
        return ftp
    except Exception as e:
        logger.error(f'Error while connecting to FTP: {e}')
        return None


def get_files_list() -> list[str]:
    with ftp_connect() as ftp:
        ftp.cwd(cfg.FTP_DIR_NAME)
        files = ftp.nlst()
        logger.info(f'{len(files)} files was received from {cfg.FTP_DIR_NAME}')
        return files


async def check_ftp_files_for_all(bot: Bot):
    files_list_str = get_message_text_with_files()
    if not files_list_str:
        return
    text = files_list_str
    user_list = [user[0] for user in await db.sql_select(db.select_subscribed_users_query())]
    for user_id in user_list:
        try:
            sent_message = await bot.send_message(user_id, text)
            await db.save_message(sent_message)
        except exceptions.TelegramBadRequest as ex:
            logger.error(f'user_id = {user_id}: {ex}')


def get_message_text_with_files() -> str:
    raw_files_list = get_files_list()
    expected_files_list = [i for i in raw_files_list if cfg.FTP_FILE_EXTENSION in i]
    return f"{m.HAS_FILES}🔸 {'\n🔸 '.join(expected_files_list)}" if expected_files_list else m.NO_FILES
