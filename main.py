import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import core.config.config as cfg
import core.handlers.basic_handlers as bh
import core.handlers.command_handlers as ch
import core.handlers.message_handlers as mh
from core.config.config import bot_settings
from core.config.menu_config import set_commands
from core.filters.check_user import IsUnregisteredUser
from core.middlewares.middleware_scheduler import MiddlewareScheduler
from core.utils.callback_entity_data import CallbackEntityData
from core.utils.functions import clear_old_messages, check_ftp_files_for_all
from core.utils.states import RegistrationStates


async def start_bot(bot: Bot):
    await set_commands(bot)


async def start():
    bot = Bot(token=bot_settings.token)

    dp = Dispatcher()

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

    scheduler.add_job(clear_old_messages,
                      trigger='interval',
                      hours=cfg.CLEAR_MSG_INTERVAL_HOURS,
                      kwargs={'bot': bot})
    scheduler.add_job(check_ftp_files_for_all,
                      trigger='interval',
                      minutes=cfg.CHECK_FILES_INTERVAL_MINS,
                      kwargs={'bot': bot})

    scheduler.start()
    dp.update.middleware.register(MiddlewareScheduler(scheduler))

    # add /start and /about commands to menu
    dp.startup.register(start_bot)

    # command handlers
    dp.message.register(ch.start_command_handler, Command(commands=['start']))
    dp.message.register(ch.about_command_handler, Command(commands=['about']))
    dp.message.register(ch.send_alert_command_handler, Command(commands=['send_alert']))

    dp.callback_query.register(mh.cancel_handler, F.data == 'cancel_action')
    dp.message.register(mh.end_register_handler, RegistrationStates.PASSWORD_TYPING)
    dp.callback_query.register(mh.switch_subscribe_handler, CallbackEntityData.filter(F.action == 'switch_subscribe'))

    # valid user check
    dp.message.register(bh.wrong_user_handler, IsUnregisteredUser())

    # reply menu handlers
    dp.message.register(mh.get_dir_status_handler, F.text == '🔍Проверить сейчас')
    dp.message.register(mh.send_subscribe_prefs_handler, F.text == '⚙️Управление подпиской')

    # callback handlers
    dp.callback_query.register(mh.start_register_handler, F.data == 'register')

    # default handlers
    dp.message.register(bh.default_handler)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
