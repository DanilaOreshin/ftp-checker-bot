from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from src.config.bot_config import config as cfg
from src.services import db_manager as db


async def clear_user_state(storage, bot_id: int, user_id: int):
    target_key = StorageKey(bot_id=bot_id, chat_id=user_id, user_id=user_id)
    await FSMContext(storage=storage, key=target_key).clear()


async def is_registered(user_id: int) -> bool | None:
    result = await db.sql_select(db.check_exists_user_query(user_id))
    return result[0][0] if result and result[0] else None


def is_admin(user_id: int) -> bool:
    return user_id == cfg.BOT_ADMIN_ID
