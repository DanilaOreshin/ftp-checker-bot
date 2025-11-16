from typing import Optional

from aiogram.filters.callback_data import CallbackData


class ActionData(CallbackData, prefix='action_data'):
    action: str
    target_user_id: Optional[int] = None
    target_user_first_name: Optional[str] = None
    target_user_last_name: Optional[str] = None
