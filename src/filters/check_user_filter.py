from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.utils.functions import is_registered, is_admin


class IsUnregisteredUser(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return not await is_registered(message.from_user.id)


class IsAdminUser(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return is_admin(message.from_user.id)
