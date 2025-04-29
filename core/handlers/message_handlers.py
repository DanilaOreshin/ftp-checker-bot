from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import core.config.messages as m
import core.keyboards.keyboard_builder as kb
import core.utils.db_manager as db
import core.utils.functions as f
from core.handlers.command_handlers import start_command_handler
from core.keyboards.button import Button
from core.utils import message_sender as ms
from core.utils.callback_entity_data import CallbackEntityData
from core.utils.pass_validator import is_valid_pass
from core.utils.states import RegistrationStates


async def cancel_handler(call: CallbackQuery, state: FSMContext):
    text = m.cancel_action_text
    await state.clear()
    await ms.send_call_answer(call, text)


async def start_register_handler(call: CallbackQuery, state: FSMContext):
    text = m.send_pass_text
    await state.set_state(RegistrationStates.PASSWORD_TYPING)
    await ms.send_call_answer(call, text)


async def end_register_handler(message: Message, state: FSMContext, bot: Bot):
    db.do_sql_modify(db.insert_message_query(message.message_id, message.chat.id))
    if is_valid_pass(message.text):
        # clear previous messages
        await f.clear_chat(bot, message.chat.id)
        # collect user data and save to db
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        db.do_sql_modify(db.insert_user_query(user_id, first_name, last_name))
        text = m.success_user_create_text
        await state.clear()
        await ms.send_message_answer(message, text)
        await start_command_handler(message)
    else:
        # draw cancel button
        text = m.wrong_pass_text
        builder = kb.get_inline_keyboard([Button(text=m.cancel_button_text, callback_data='cancel_action')])
        await ms.send_message_answer_with_buttons(message, text, builder.as_markup())


async def get_dir_status_handler(message: Message, bot: Bot):
    # clear previous messages
    await f.clear_chat(bot, message.chat.id)
    # check and send notification
    await f.check_ftp_files_for_one_user(message)


async def switch_subscribe_handler(call: CallbackQuery, callback_data: CallbackEntityData):
    previous_button_text = call.message.reply_markup.inline_keyboard[0][0].text
    if previous_button_text == m.subscribe_button_text:
        next_button_text = m.unsubscribe_button_text
        next_message_text = m.subscribe_message_text
        db.do_sql_modify(db.update_subscribe_query(callback_data.entity_id, 1))
    else:
        next_button_text = m.subscribe_button_text
        next_message_text = m.unsubscribe_message_text
        db.do_sql_modify(db.update_subscribe_query(callback_data.entity_id, 0))
    # redraw buttons
    builder = kb.get_inline_keyboard([Button(text=next_button_text,
                                             callback_data=CallbackEntityData(action='switch_subscribe',
                                                                              entity_id=callback_data.entity_id))])
    await call.message.edit_text(text=next_message_text, parse_mode='HTML', reply_markup=builder.as_markup())
    await call.answer()


async def send_subscribe_prefs_handler(message: Message):
    user_id = message.from_user.id
    db.do_sql_modify(db.insert_message_query(message.message_id, user_id))
    res = db.do_sql_select(db.select_sub_user_query(user_id))
    is_subscribe = int(res[0][0])
    button_text = m.unsubscribe_button_text if is_subscribe == 1 else m.subscribe_button_text
    message_text = m.subscribe_message_text if is_subscribe == 1 else m.unsubscribe_message_text
    inline_builder = kb.get_inline_keyboard(
        [Button(text=button_text, callback_data=CallbackEntityData(action='switch_subscribe', entity_id=user_id))])
    await ms.send_message_answer_with_buttons(message, message_text, inline_builder.as_markup())
