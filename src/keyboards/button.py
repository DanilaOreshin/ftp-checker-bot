from dataclasses import dataclass
from typing import Optional

from aiogram.filters.callback_data import CallbackData


@dataclass
class Button:
    text: str
    callback_data: Optional[CallbackData] = None
