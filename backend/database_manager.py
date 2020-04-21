import uuid
import datetime

from datetime import datetime as dt

from general_falcon_webserver.backend.general_manager.databases import SqliteDatabase

TIME_FORMAT = '%d/%m/%Y %H:%M:%S'
TIME_EXPIRE = 600


class DatabaseManager:
    def __init__(self, db: SqliteDatabase):
        self.db = db

    def sign_in_or_create_oauth_user(self, userid: str):
        self.db.send_query(f"INSERT INTO users(userid) "
                           f"SELECT {userid} "
                           f"WHERE NOT EXISTS(SELECT 1 FROM users WHERE userid={userid})")

        token = uuid.uuid4().hex
        self.db.send_query(f"REPLACE INTO users(session_id, session_timeout) "
                           f"VALUES ('{token}', "
                           f"'{(dt.now() + datetime.timedelta(0, TIME_EXPIRE)).strftime(TIME_FORMAT)}')")

        return token
