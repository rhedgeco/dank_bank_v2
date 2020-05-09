import uuid
import datetime
import falcon

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
        self.db.send_query(f"REPLACE INTO users(userid, session_id, session_timeout) "
                           f"VALUES ('{userid}', '{token}', "
                           f"'{(dt.now() + datetime.timedelta(0, TIME_EXPIRE)).strftime(TIME_FORMAT)}')")

        return token

    def create_new_group(self, session: str, group_name: str):
        user = self._get_user_from_database(session)
        group_id = uuid.uuid4().hex
        self.db.send_query(f"INSERT INTO groups(groupid, name) "
                           f"VALUES ('{group_id}', '{group_name}')")
        self.db.send_query(f"INSERT INTO users_groups (user_id, group_id) "
                           f"VALUES ('{user['userid']}', '{group_id}')")

    def create_transaction(self, session: str, group_id: str, amount: float, paid: str, desc: str = ""):
        user = self._get_user_from_database(session)
        trans_id = uuid.uuid4().hex
        self.db.send_query(f"INSERT INTO transactions (transid, groupid, user_pay, users_paid, amount, description) "
                           f"VALUES ('{trans_id}', '{group_id}', '{user['user_id']}', '{paid}', '{amount}', '{desc}')")

    def get_user_info(self, session: str):
        user = self._get_user_from_database(session)
        groups = self.db.fetchall_query(f"SELECT * FROM users_groups WHERE user_id='{user['userid']}'")

        group_ids = []
        for group in groups:
            group_ids.append(group['group_id'])

        user = {
            "nickname": user['nickname'],
            "groups": group_ids
        }

        return user

    def get_group_info(self, session: str, group_id: str):
        group = self._validate_user_group(session, group_id)
        trans = self.db.fetchall_query(f"SELECT * FROM transactions WHERE groupid='{group_id}'")
        group_info = {
            'group_name': group['name'],
            'transactions': trans
        }
        return group_info

    def _get_user_from_database(self, session: str):
        user = self.db.fetchone_query(f"SELECT * FROM users WHERE session_id='{session}'")
        if not user:
            raise falcon.HTTPBadRequest('Could not validate session')
        self._validate_user_session(user['userid'])
        return user

    def _validate_user_group(self, session: str, groupid: str):
        user = self._get_user_from_database(session)
        group_check = self.db.fetchone_query(
            f"SELECT * FROM users_groups WHERE user_id='{user['userid']}' AND group_id='{groupid}'")
        if not group_check:
            raise falcon.HTTPUnauthorized('User does not hae access to this group.')
        group = self.db.fetchone_query(f"SELECT * FROM groups WHERE groupid='{groupid}'")
        return group

    def _validate_user_session(self, userid: str):
        user = self.db.fetchone_query(f"SELECT * FROM users WHERE userid = '{userid}'")
        if not user:
            raise falcon.HTTPBadRequest('User ID not accepted.')

        user_expire = dt.strptime(user['session_timeout'], TIME_FORMAT)
        if user_expire < dt.now():
            raise falcon.HTTPUnauthorized(f'User session has timed out.')
        session = user['session_id']
        self.db.send_query(f"REPLACE INTO users(userid, session_id, session_timeout) "
                           f"VALUES ('{userid}', '{session}', "
                           f"'{(dt.now() + datetime.timedelta(0, TIME_EXPIRE)).strftime(TIME_FORMAT)}')")
