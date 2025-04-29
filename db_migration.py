import core.utils.db_manager as db

CREATE_TUSER = '''CREATE TABLE tuser (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    first_name TEXT,
                    last_name TEXT,
                    is_subscribe INTEGER DEFAULT (1) NOT NULL,
                    create_date INTEGER NOT NULL
                    );'''

CREATE_TUSER_INDEX = 'CREATE UNIQUE INDEX tuser_user_id_IDX ON tuser (user_id);'

CREATE_TMESSAGES = '''CREATE TABLE tmessages (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        message_id INTEGER NOT NULL,
                        chat_id INTEGER NOT NULL,
                        create_date INTEGER NOT NULL);'''

CREATE_TMESSAGES_INDEX = 'CREATE INDEX tmessages_chat_id_IDX ON tmessages (chat_id);'

db.do_sql_modify(CREATE_TMESSAGES)
db.do_sql_modify(CREATE_TMESSAGES_INDEX)
db.do_sql_modify(CREATE_TUSER)
db.do_sql_modify(CREATE_TUSER_INDEX)
