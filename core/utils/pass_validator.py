import hashlib

from core.config.config import bot_settings


def is_valid_pass(password: str):
    return hashlib.md5(password.encode()).hexdigest() == bot_settings.password
