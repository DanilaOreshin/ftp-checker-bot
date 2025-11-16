from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

import src.services.db_manager as db
from src.services.message_manager import clear_target_chat


class SaveMessagesMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]
                       ) -> Any:
        bot = data.get("bot")
        if bot:
            await clear_target_chat(bot, event.chat.id)

        await db.save_message(event)
        return await handler(event, data)
