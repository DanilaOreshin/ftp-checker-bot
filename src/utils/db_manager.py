from aiogram.types import Message
from sqlalchemy import text, TextClause
from sqlalchemy.ext.asyncio import create_async_engine

from src.config.bot_settings import settings as cfg

async_engine = create_async_engine(url=cfg.DATABASE_URL,
                                   echo=False,
                                   pool_size=10,
                                   max_overflow=5)


async def sql_modify(statement: TextClause):
    async with async_engine.connect() as conn:
        await conn.execute(statement)
        await conn.commit()


async def sql_select(statement: TextClause):
    async with async_engine.connect() as conn:
        res = await conn.execute(statement)
        return res.all()


async def save_message(message: Message):
    await sql_modify(insert_message_query(message.message_id, message.chat.id))


def check_exists_user_query(user_id: int) -> TextClause:
    query = '''SELECT EXISTS (SELECT * FROM db_ftp_checker.tuser tu WHERE tu.user_id = :user_id) AS res;'''
    return text(query).bindparams(user_id=user_id)


def insert_user_query(user_id: int, first_name: str, last_name: str) -> TextClause:
    query = '''INSERT INTO db_ftp_checker.tuser(user_id, first_name, last_name) 
                VALUES (:user_id, :first_name, :last_name);'''
    return text(query).bindparams(user_id=user_id,
                                  first_name=first_name,
                                  last_name=last_name)


def select_subscribed_users_query():
    query = '''SELECT tu.user_id FROM db_ftp_checker.tuser tu WHERE tu.is_subscribe = true;'''
    return text(query)


def select_all_users_query():
    query = '''SELECT tu.user_id FROM db_ftp_checker.tuser tu;'''
    return text(query)


def select_sub_user_query(user_id: int):
    query = '''SELECT tu.is_subscribe FROM db_ftp_checker.tuser tu WHERE tu.user_id = :user_id;'''
    return text(query).bindparams(user_id=user_id)


def update_subscribe_query(user_id: int, is_subscribe: int):
    query = '''UPDATE db_ftp_checker.tuser
                SET is_subscribe = :is_subscribe
                WHERE user_id = :user_id;'''
    return text(query).bindparams(is_subscribe=is_subscribe,
                                  user_id=user_id)


def insert_message_query(message_id: int, chat_id: int) -> TextClause:
    query = '''INSERT INTO db_ftp_checker.tmessage (message_id, chat_id) VALUES (:message_id, :chat_id);'''
    return text(query).bindparams(message_id=message_id,
                                  chat_id=chat_id)


def select_messages_query(chat_id: int) -> TextClause:
    query = '''SELECT tm.message_id FROM db_ftp_checker.tmessage tm WHERE tm.chat_id = :chat_id;'''
    return text(query).bindparams(chat_id=chat_id)


def delete_messages_by_chat_id_query(chat_id: int) -> TextClause:
    query = '''DELETE FROM db_ftp_checker.tmessage WHERE chat_id = :chat_id;'''
    return text(query).bindparams(chat_id=chat_id)


def select_old_messages_query(interval: str) -> TextClause:
    query = f'''SELECT tm.chat_id, tm.message_id FROM db_ftp_checker.tmessage tm 
                WHERE tm.create_date < now() - INTERVAL '{interval}';'''
    return text(query)


def delete_messages_by_message_ids_query(message_ids: list) -> TextClause:
    query = '''DELETE FROM db_ftp_checker.tmessage WHERE message_id = ANY(:message_ids);'''
    return text(query).bindparams(message_ids=message_ids)
