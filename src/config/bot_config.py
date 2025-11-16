import os

from dotenv import load_dotenv


class BotConfig:
    def __init__(self) -> None:

        load_dotenv()

        self.BOT_TOKEN = self._get_required("BOT_TOKEN")
        self.BOT_ADMIN_ID = int(self._get_required('BOT_ADMIN_ID'))
        self.BOT_DEVELOPER = self._get_required('BOT_DEVELOPER')
        self.BOT_VERSION = self._get_required('BOT_VERSION')

        self.DB_HOST = self._get_required('DB_HOST')
        self.DB_PORT = self._get_required('DB_PORT')
        self.DB_USER = self._get_required("DB_USER")
        self.DB_PASSWORD = self._get_required('DB_PASSWORD')
        self.DB_NAME = self._get_required("DB_NAME")

        self.FTP_HOST = self._get_required("FTP_HOST")
        self.FTP_PORT = int(self._get_required('FTP_PORT'))
        self.FTP_USER = self._get_required('FTP_USER')
        self.FTP_PASSWORD = self._get_required('FTP_PASSWORD')
        self.FTP_DIR_NAME = self._get_required("FTP_DIR_NAME")
        self.FTP_FILE_EXTENSION = self._get_required('FTP_FILE_EXTENSION')

        self.INTERVAL_CLEAR_MSG_HOURS = int(self._get_required("INTERVAL_CLEAR_MSG_HOURS"))
        self.INTERVAL_CHECK_FILES_MINUTES = int(self._get_required('INTERVAL_CHECK_FILES_MINUTES'))
        self.INTERVAL_OLD_MSG_PERIOD = self._get_required('INTERVAL_OLD_MSG_PERIOD')

    @property
    def DATABASE_URL(self) -> str:
        # postgresql+asyncpg://postgres:postgres@localhost:5432/postgres
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @staticmethod
    def _get_required(key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Missing required environment variable: {key}")
        return value

    # def _get_optional(self, key: str, default: any = None, type_cast: type = str) -> any:
    #     value = os.getenv(key)
    #     if value is None:
    #         return default
    #     try:
    #         return type_cast(value) if type_cast else value
    #     except (ValueError, TypeError):
    #         return default

    def __str__(self) -> str:
        attributes = {}
        for key, value in self.__dict__.items():
            attributes[key] = value

        attrs_str = ', '.join(f"{k}={v}" for k, v in attributes.items())
        return f"Config({attrs_str})"


config = BotConfig()
