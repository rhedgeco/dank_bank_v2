import falcon

from general_falcon_webserver.backend.general_manager.databases import SqliteDatabase


class DatabaseManager:
    def __init__(self, db: SqliteDatabase):
        self.db = db

    def sign_in_or_create_oauth_user(self, userid: str):
        self.db.send_query(f'INSERT INTO google_oauth(userid) '
                           f'SELECT {userid} '
                           f'WHERE NOT EXISTS(SELECT 1 FROM google_oauth WHERE userid={userid})')
