from aiogram.types import User
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from src.entity.action_data import ActionData
from src.keyboards import keyboard_builder as kb
from src.keyboards.button import Button
from src.texts import messages_texts as m
from src.texts.buttons_texts import BUTTONS


def request_access_component(user: User) -> tuple[str, InlineKeyboardBuilder]:
    user_data = {'target_user_id': user.id,
                 'target_user_first_name': user.first_name,
                 'target_user_last_name': user.last_name}
    message_text = m.REQUEST_ACCESS.format(target_user_nickname=user.username, **user_data)
    buttons = [
        Button(text=BUTTONS['accept_request'], callback_data=ActionData(action='accept_request', **user_data)),
        Button(text=BUTTONS['decline_request'], callback_data=ActionData(action='decline_request', **user_data))
    ]
    return message_text, kb.get_inline_keyboard(buttons)


def current_settings_component(user_id: int, is_subscribed: bool) -> tuple[str, InlineKeyboardBuilder]:
    button_text = BUTTONS['unsubscribe'] if is_subscribed else BUTTONS['subscribe']
    message_text = m.SUBSCRIBED if is_subscribed else m.UNSUBSCRIBED
    buttons = [Button(text=button_text, callback_data=ActionData(action='switch_subscribe', target_user_id=user_id))]
    return message_text, kb.get_inline_keyboard(buttons)


def welcome_message_component() -> tuple[str, ReplyKeyboardBuilder]:
    message_text = m.WELCOME
    buttons = [Button(text=BUTTONS['check']), Button(text=BUTTONS['preferences'])]
    return message_text, kb.get_reply_keyboard(buttons)


def start_registration_component() -> tuple[str, InlineKeyboardBuilder]:
    message_text = m.START_COMMAND
    buttons = [Button(text=BUTTONS['registration'], callback_data=ActionData(action='register'))]
    return message_text, kb.get_inline_keyboard(buttons)
