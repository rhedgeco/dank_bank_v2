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

    def sign_in_or_create_oauth_user(self, userid: str, nickname: str):
        self.db.send_query(f"INSERT OR IGNORE INTO users (userid, nickname) VALUES ('{userid}', '{nickname}')")
        session = uuid.uuid4().hex
        self._reset_user_session(userid, session)
        return session

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
                           f"VALUES ('{trans_id}', '{group_id}', '{user['userid']}', '{paid}', '{amount}', '{desc}')")

    def get_transactions(self, session:str, groupid:str):
        self._validate_user_session(session)
        return self._get_transactions(groupid)


    def get_user_info(self, session: str):
        user = self._get_user_from_database(session)
        groups = self.db.fetchall_query(f"SELECT * FROM users_groups WHERE user_id='{user['userid']}'")

        group_ids = []
        for g in groups:
            group = self.db.fetchone_query(f"SELECT * FROM groups WHERE groupid = '{g['group_id']}'")
            group_ids.append({
                g['group_id']: group['name']
            })

        user = {
            "nickname": user['nickname'],
            "groups": group_ids
        }

        return user

    def get_group_info(self, session: str, group_id: str):
        group = self._validate_user_group(session, group_id)

        users_groups = self.db.fetchall_query(f"SELECT * FROM users_groups WHERE group_id='{group_id}'")
        users = []
        for u in users_groups:
            user = self.db.fetchone_query(f"SELECT * FROM users WHERE userid='{u['user_id']}'")
            users.append({
                user['userid']: user['nickname']
            })

        trans = self._get_transactions(group_id)
        for t in trans:
            del t['transid']
            del t['groupid']

        group_info = {
            'group_name': group['name'],
            'users': users,
            'transactions': trans
        }
        return group_info

    def _get_transactions(self, group_id: str):
        return self.db.fetchall_query(f"SELECT * FROM transactions WHERE groupid='{group_id}'")

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
        self._reset_user_session(userid, session)

    def _reset_user_session(self, userid: str, session: str):
        self.db.send_query(f"UPDATE users SET session_id='{session}', "
                           f"session_timeout='{(dt.now() + datetime.timedelta(0, TIME_EXPIRE)).strftime(TIME_FORMAT)}' "
                           f"WHERE userid='{userid}'")
