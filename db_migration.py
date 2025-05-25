import asyncio

from sqlalchemy import text

import src.utils.db_manager as db

CREATE_TUSER = '''CREATE TABLE db_ftp_checker.tuser (
    id bigserial NOT NULL,
    user_id int8 NOT NULL,
    first_name varchar(100) NULL,
    last_name varchar(100) NULL,
    is_subscribe bool DEFAULT true NOT NULL,
    create_date timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT pk_tuser_id PRIMARY KEY (id),
    CONSTRAINT un_tuser_user_id UNIQUE (user_id)
);'''

CREATE_TUSER_USER_ID_INDEX = '''CREATE INDEX idx_tuser_user_id ON db_ftp_checker.tuser USING btree (user_id);'''

CREATE_TMESSAGE = '''CREATE TABLE db_ftp_checker.tmessage (
    id bigserial NOT NULL,
    message_id int8 NOT NULL,
    chat_id int8 NOT NULL,
    create_date timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT pk_tmessage_id PRIMARY KEY (id)
);'''

CREATE_TMESSAGE_CHAT_ID_INDEX = '''CREATE INDEX idx_tmessage_chat_id ON db_ftp_checker.tmessage 
                                                                                      USING btree (chat_id);'''


async def migrate():
    await db.sql_modify(text(CREATE_TUSER))
    await db.sql_modify(text(CREATE_TUSER_USER_ID_INDEX))
    await db.sql_modify(text(CREATE_TMESSAGE))
    await db.sql_modify(text(CREATE_TMESSAGE_CHAT_ID_INDEX))


asyncio.run(migrate())
