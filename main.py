import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import src.handlers.basic_handlers as bh
import src.handlers.command_handlers as ch
import src.handlers.message_handlers as mh
from src.config.bot_config import config as cfg
from src.config.menu_config import set_commands
from src.entity.action_data import ActionData
from src.entity.states import RegistrationStates
from src.filters.check_user_filter import IsUnregisteredUser, IsAdminUser
from src.middlewares.save_messages_middleware import SaveMessagesMiddleware
from src.middlewares.scheduler_middleware import SchedulerMiddleware
from src.services.ftp_manager import check_ftp_files_for_all
from src.services.message_manager import clear_old_messages


async def start_bot(bot: Bot):
    await set_commands(bot)


async def start():
    bot = Bot(token=cfg.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

    scheduler.add_job(clear_old_messages,
                      trigger='interval',
                      hours=cfg.INTERVAL_CLEAR_MSG_HOURS,
                      kwargs={'bot': bot})
    scheduler.add_job(check_ftp_files_for_all,
                      trigger='interval',
                      minutes=cfg.INTERVAL_CHECK_FILES_MINUTES,
                      kwargs={'bot': bot})

    scheduler.start()
    dp.update.middleware.register(SchedulerMiddleware(scheduler))
    dp.message.middleware(SaveMessagesMiddleware())

    # add commands to menu
    dp.startup.register(start_bot)

    dp.message.register(ch.start_command_handler, Command(commands=['start']))

    dp.message.register(mh.waiting_handler, RegistrationStates.WAITING)

    # valid user check
    dp.message.register(bh.wrong_user_handler, IsUnregisteredUser())

    # command handlers
    dp.message.register(ch.help_command_handler, Command(commands=['help']))
    dp.message.register(ch.about_command_handler, Command(commands=['about']))
    dp.message.register(ch.alert_command_handler, Command(commands=['alert']), IsAdminUser())

    dp.callback_query.register(mh.request_access_handler, ActionData.filter(F.action == 'register'))
    dp.callback_query.register(mh.accept_access_handler, ActionData.filter(F.action == 'accept_request'))
    dp.callback_query.register(mh.decline_access_handler, ActionData.filter(F.action == 'decline_request'))

    dp.callback_query.register(mh.switch_subscribe_handler, ActionData.filter(F.action == 'switch_subscribe'))

    # reply menu handlers
    dp.message.register(mh.manual_check_handler, F.text == '🔍Проверить сейчас')
    dp.message.register(mh.current_settings_handler, F.text == '⚙️Управление подпиской')

    # default handlers
    dp.message.register(bh.default_handler)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
