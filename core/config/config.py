from dataclasses import dataclass

CLEAR_MSG_INTERVAL_HOURS = 1
CHECK_FILES_INTERVAL_MINS = 15

TIMESTAMP_1_DAY = 86400
OLD_MESSAGE_DELAY = TIMESTAMP_1_DAY / 2

BOT_AUTHOR = '@Danila_Oreshin'
BOT_VERSION = '1.1.0 Release'
BOT_TOKEN = ''
BOT_PASSWORD_MD5 = '5f3ab2c4f0b0689e83fcda6'

DB_PATH = 'resources/db/db_ftp_checker.db'

FTP_HOST = 'ftp.test.ru'
FTP_PORT = 21
FTP_LOGIN = ''
FTP_PASSWORD = ''
FTP_DIR_NAME = ''

FTP_FILE_EXTENSION = '.indd'


@dataclass
class BotSettings:
    token: str
    password: str


def get_settings():
    return BotSettings(token=BOT_TOKEN, password=BOT_PASSWORD_MD5)


bot_settings = get_settings()
