import hashlib

from src.config.bot_settings import settings as cfg


def is_valid_pass(password: str):
    return hashlib.md5(password.encode()).hexdigest() == cfg.BOT_MASTER_PASSWORD
