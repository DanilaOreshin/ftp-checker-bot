from aiogram.filters import BaseFilter
from aiogram.types import Message

from core.utils.db_manager import do_sql_select, check_exists_user_query


def is_registered(user_id: int):
    return do_sql_select(check_exists_user_query(user_id))[0][0]


class IsUnregisteredUser(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        return not is_registered(user_id)
