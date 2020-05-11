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

    def sign_in_or_create_oauth_user(self, user_id: str, nickname: str, photo: str):
        self.db.send_query(f"INSERT OR IGNORE INTO users (user_id, nickname, photo) "
                           f"VALUES ('{user_id}', '{nickname}', '{photo}')")
        session = uuid.uuid4().hex
        self._reset_user_session(user_id, session)
        return session

    def create_new_group(self, session: str, group_name: str):
        user = self._get_user_from_database(session)
        group_id = uuid.uuid4().hex
        self.db.send_query(f"INSERT INTO groups(group_id, name) "
                           f"VALUES ('{group_id}', '{group_name}')")
        self.db.send_query(f"INSERT INTO users_groups (user_id, group_id) "
                           f"VALUES ('{user['user_id']}', '{group_id}')")

    def create_transaction(self, session: str, group_id: str, amount: float, paid: str, desc: str = ""):
        user = self._get_user_from_database(session)
        trans_id = uuid.uuid4().hex
        self.db.send_query(f"INSERT INTO transactions (trans_id, group_id, user_pay, users_paid, amount, description) "
                           f"VALUES ('{trans_id}', '{group_id}', '{user['user_id']}', '{paid}', '{amount}', '{desc}')")

    def get_transactions(self, session: str, group_id: str):
        self._validate_user_session(session)
        return self._get_transactions(group_id)

    def get_user_info(self, session: str):
        user = self._get_user_from_database(session)
        groups = self.db.fetchall_query(f"SELECT * FROM users_groups WHERE user_id='{user['user_id']}'")

        group_ids = []
        for g in groups:
            group = self.db.fetchone_query(f"SELECT * FROM groups WHERE group_id = '{g['group_id']}'")
            group_ids.append({
                g['group_id']: group['name']
            })

        user = {
            "id": user['user_id'],
            "nickname": user['nickname'],
            "photo": user['photo'],
            "groups": group_ids
        }

        return user

    def get_group_info(self, session: str, group_id: str):
        group = self._validate_user_group(session, group_id)

        users_groups = self.db.fetchall_query(f"SELECT * FROM users_groups WHERE group_id='{group_id}'")
        users = []
        for u in users_groups:
            user = self.db.fetchone_query(f"SELECT * FROM users WHERE user_id='{u['user_id']}'")
            users.append({
                user['user_id']: user['nickname']
            })

        trans = self._get_transactions(group_id)
        for t in trans:
            del t['trans_id']
            del t['group_id']

        group_info = {
            'group_name': group['name'],
            'users': users,
            'transactions': trans,
            'debts': [
                {
                    'from': 12345,
                    'from_name': 'Ryan Hedgecock',
                    'to': 54321,
                    'to_name': 'Danny Giap',
                    'amount': 100.00
                },
                {
                    'from': 51423,
                    'from_name': 'Jeevanesh',
                    'to': 12345,
                    'to_name': 'Danny Giap',
                    'amount': 169.00
                }
            ]
        }
        return group_info

    def _get_transactions(self, group_id: str):
        return self.db.fetchall_query(f"SELECT * FROM transactions WHERE group_id='{group_id}'")

    def _get_user_from_database(self, session: str):
        user = self.db.fetchone_query(f"SELECT * FROM users WHERE session_id='{session}'")
        if not user:
            raise falcon.HTTPBadRequest('Could not validate session')
        self._validate_user_session(user['user_id'])
        return user

    def _validate_user_group(self, session: str, group_id: str):
        user = self._get_user_from_database(session)
        group_check = self.db.fetchone_query(
            f"SELECT * FROM users_groups WHERE user_id='{user['user_id']}' AND group_id='{group_id}'")
        if not group_check:
            raise falcon.HTTPUnauthorized('User does not hae access to this group.')
        group = self.db.fetchone_query(f"SELECT * FROM groups WHERE group_id='{group_id}'")
        return group

    def _validate_user_session(self, user_id: str):
        user = self.db.fetchone_query(f"SELECT * FROM users WHERE user_id = '{user_id}'")
        if not user:
            raise falcon.HTTPBadRequest('User ID not accepted.')

        user_expire = dt.strptime(user['session_timeout'], TIME_FORMAT)
        if user_expire < dt.now():
            raise falcon.HTTPUnauthorized(f'User session has timed out.')
        session = user['session_id']
        self._reset_user_session(user_id, session)

    def _reset_user_session(self, user_id: str, session: str):
        self.db.send_query(f"UPDATE users SET session_id='{session}', "
                           f"session_timeout='{(dt.now() + datetime.timedelta(0, TIME_EXPIRE)).strftime(TIME_FORMAT)}' "
                           f"WHERE user_id='{user_id}'")
