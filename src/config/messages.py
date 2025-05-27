from src.config.bot_settings import settings as cfg

not_registered_text = f'Ты - незарегистрированный пользователь!!!\n' \
                      f'\n' \
                      f'Введи /start для запуска процесса регистрации.'

welcome_text = f'Добро пожаловать! 🎉\n ' \
               f'\n' \
               f'Ниже будут появляться сообщения в случае, если на сервере {cfg.FTP_HOST}, ' \
               f'в директории <b>{cfg.FTP_DIR_NAME}</b> будут файлы с расширением <b>{cfg.FTP_FILE_EXTENSION}</b>.\n' \
               f'\n' \
               f'Также можно выполнить ручную проверку, нажав на кнопку <b>"Проверить сейчас"</b>.'

about_text = f'О боте:\n' \
             f'\n' \
             f'Версия: {cfg.BOT_VERSION}\n' \
             f'Автор: {cfg.BOT_DEVELOPER}\n' \
             f'\n' \
             f'Описание: Бот для проверки наличия файлов на FTP-сервере.'

start_registration_text = f'Вы не зарегистрированы!\n' \
                          f'Для начала работы нужно пройти регистрацию 👇'

default_text = f'Неверное действие!\n' \
               f'\n' \
               f'Скорее всего ты видишь это сообщение, потому что пишешь отсебятину, но это не chatGPT 🙃\n' \
               f'\n' \
               f'Нажми на доступные кнопки или отправь /start'

cancel_action_text = f'Действие отменено!'

send_pass_text = f'Пришли пароль 🔐'

success_user_create_text = f'Пользователь успешно зарегистрирован!'

wrong_pass_text = f'Неверный пароль!\n' \
                  f'\n' \
                  f'Пришли новый пароль или отмени регистрацию 👇'

cancel_button_text = '❌Отменить'

nothing_into_dir_text = f'В директории <b>{cfg.FTP_DIR_NAME}</b> пока нет ' \
                        f'файлов с расширением <b>{cfg.FTP_FILE_EXTENSION}</b> 🙁'

have_files_text = f'В директории <b>{cfg.FTP_DIR_NAME}</b> есть файлы с ' \
                  f'расширением <b>{cfg.FTP_FILE_EXTENSION}</b>!\n' \
                  f'\n'

subscribe_button_text = f'✅Подписаться'

unsubscribe_button_text = f'❌Отписаться'

subscribe_message_text = f'Ты подписан на автоматическую рассылку!\n' \
                         f'\n' \
                         f'Бот будет проверять наличие файлов с расширением <b>{cfg.FTP_FILE_EXTENSION}</b> ' \
                         f'в директории <b>{cfg.FTP_DIR_NAME}</b> раз в {cfg.INTERVAL_CHECK_FILES_MINUTES} минут и ' \
                         f'отправлять тебе сообщение, если в директории будет хоть 1 подходящий файл.\n' \
                         f'\n' \
                         f'Чтобы отписаться от автоматической рассылки, нажми кнопку ниже.'

unsubscribe_message_text = f'Ты НЕ подписан на автоматическую рассылку!\n' \
                           f'\n' \
                           f'Бот НЕ будет отправлять тебе автоматические нотификации.\n' \
                           f'\n' \
                           f'Чтобы подписаться не автоматическую рассылку, нажми кнопку ниже.'
