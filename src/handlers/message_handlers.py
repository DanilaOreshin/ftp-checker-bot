from typing import Optional

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import src.services.db_manager as db
import src.texts.messages_texts as m
from src.config.bot_config import config as cfg
from src.entity.action_data import ActionData
from src.entity.states import RegistrationStates
from src.services.ftp_manager import get_message_text_with_files
from src.services.message_manager import send_message_answer, send_call_answer
from src.utils.components import request_access_component, current_settings_component, welcome_message_component
from src.utils.functions import clear_user_state


async def request_access_handler(call: CallbackQuery, state: FSMContext, bot: Bot):
    await state.set_state(RegistrationStates.WAITING)
    await send_call_answer(call, m.REQUEST_SENT)
    text_for_admin, builder = request_access_component(call.from_user)
    sent_message = await bot.send_message(cfg.BOT_ADMIN_ID, text_for_admin, reply_markup=builder.as_markup())
    await db.save_message(sent_message)


async def waiting_handler(message: Optional[Message] = None, call: Optional[CallbackQuery] = None):
    if message:
        await send_message_answer(message, m.WAIT)
    if call:
        await send_call_answer(call, m.WAIT)


async def accept_access_handler(call: CallbackQuery, callback_data: ActionData, state: FSMContext, bot: Bot):
    user_data = {'user_id': callback_data.target_user_id,
                 'user_first_name': callback_data.target_user_first_name,
                 'user_last_name': callback_data.target_user_last_name}
    await db.sql_modify(db.insert_user_query(**user_data))
    await send_call_answer(call, m.ACCESS_GRANTED)
    text, builder = welcome_message_component()
    await bot.send_message(user_data['user_id'], text, reply_markup=builder.as_markup(resize_keyboard=True))
    await clear_user_state(state.storage, state.key.bot_id, user_data['user_id'])


async def decline_access_handler(call: CallbackQuery, callback_data: ActionData, state: FSMContext, bot: Bot):
    await send_call_answer(call, m.ACCESS_DENIED)
    sent_message = await bot.send_message(callback_data.target_user_id, m.REQUEST_REJECTED)
    await db.save_message(sent_message)
    await clear_user_state(state.storage, state.key.bot_id, callback_data.target_user_id)


async def manual_check_handler(message: Message):
    files_list_str = get_message_text_with_files()
    text = files_list_str if files_list_str else m.NO_FILES
    await send_message_answer(message, text)


async def switch_subscribe_handler(call: CallbackQuery, callback_data: ActionData):
    user_id = callback_data.target_user_id
    is_subscribed = not bool((await db.sql_select(db.select_subscribe_by_user_query(user_id)))[0][0])
    await db.sql_modify(db.update_subscribe_query(user_id, is_subscribed))
    message_text, builder = current_settings_component(user_id, is_subscribed)
    await call.message.edit_text(text=message_text, reply_markup=builder.as_markup())
    await call.answer()


async def current_settings_handler(message: Message):
    user_id = message.from_user.id
    is_subscribed = (await db.sql_select(db.select_subscribe_by_user_query(user_id)))[0][0]
    message_text, builder = current_settings_component(user_id, is_subscribed)
    await send_message_answer(message, message_text, builder.as_markup())
