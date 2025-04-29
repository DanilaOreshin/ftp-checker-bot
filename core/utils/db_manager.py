import sqlite3
import time

import core.config.config as cfg


def get_connection(db_path: str):
    return sqlite3.connect(db_path)


def do_sql_modify(sql_query: str):
    conn = get_connection(cfg.DB_PATH)
    conn.cursor().execute(sql_query)
    conn.commit()
    conn.close()


def do_sql_select(sql_query: str):
    conn = get_connection(cfg.DB_PATH)
    result = conn.cursor().execute(sql_query).fetchall()
    conn.close()
    return result


def check_exists_user_query(user_id: int):
    return f'''SELECT EXISTS (SELECT * FROM tuser tu WHERE tu.user_id = {user_id}) AS res;'''


def insert_user_query(user_id: int, first_name: str, last_name: str):
    create_date = int(time.time())
    return f'''INSERT INTO tuser(user_id, first_name, last_name, create_date)
                VALUES ({user_id},'{first_name}','{last_name}',{create_date});'''


def select_subscribed_users_query():
    return f'''SELECT tu.user_id FROM tuser tu WHERE tu.is_subscribe = true;'''


def select_all_users_query():
    return f'''SELECT tu.user_id FROM tuser tu;'''


def select_sub_user_query(user_id: int):
    return f'''SELECT tu.is_subscribe FROM tuser tu WHERE tu.user_id = {user_id};'''


def insert_message_query(message_id: int, chat_id: int):
    create_date = int(time.time())
    return f'''INSERT INTO tmessages (message_id, chat_id, create_date)
                VALUES ({message_id},{chat_id},{create_date});'''


def select_messages_query(chat_id: int):
    return f'''SELECT tm.message_id FROM tmessages tm WHERE tm.chat_id = {chat_id};'''


def delete_messages_by_chat_id_query(chat_id: int):
    return f'''DELETE FROM tmessages WHERE chat_id = {chat_id};'''


def select_old_messages_query():
    last_day_datetime = int(time.time()) - cfg.OLD_MESSAGE_DELAY
    return f'''SELECT tm.chat_id, tm.message_id FROM tmessages tm WHERE tm.create_date <= {last_day_datetime};'''


def delete_messages_by_message_ids_query(message_ids: str):
    return f'''DELETE FROM tmessages WHERE message_id IN ({message_ids});'''


def update_subscribe_query(user_id: int, is_subscribe: int):
    return f'''UPDATE tuser
                SET is_subscribe = {is_subscribe}
                WHERE user_id = {user_id};'''
