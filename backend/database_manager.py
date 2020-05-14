import uuid
import datetime
from typing import List

import falcon

from datetime import datetime as dt

from general_falcon_webserver.backend.general_manager.databases import SqliteDatabase

from backend.data_management.debt_transfer import Transaction, Debt, transactions_to_debt

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
        return group_id

    def add_user_to_group(self, session: str, group_id: str):
        user = self._get_user_from_database(session)
        if not self._validate_group_exists(group_id):
            raise falcon.HTTPUnauthorized('Group does not exist')

        self.db.send_query(f"INSERT INTO users_groups(user_id, group_id) "
                           f"VALUES ('{user['user_id']}', '{group_id}')")

    def delete_group(self, session: str, group_id: str):
        user = self._get_user_from_database(session)
        if not self._validate_user_in_group(user['user_id'], group_id):
            raise falcon.HTTPUnauthorized('Group does not exist')

        self.db.send_query(f"DELETE FROM groups WHERE group_id = '{group_id}'")
        self.db.send_query(f"DELETE FROM users_groups WHERE group_id = '{group_id}'")
        self.db.send_query(f"DELETE FROM transactions WHERE group_id = '{group_id}'")

    def create_transaction(self, session: str, group_id: str, amount: float, paid: str, desc: str = ""):
        user = self._get_user_from_database(session)
        trans_id = uuid.uuid4().hex
        self.db.send_query(f"INSERT INTO transactions (trans_id, group_id, user_pay, users_paid, amount, description) "
                           f"VALUES ('{trans_id}', '{group_id}', '{user['user_id']}', '{paid}', '{amount}', '{desc}')")

    def get_transactions(self, session: str, group_id: str):
        user = self.db.fetchone_query(f"SELECT * FROM users WHERE session_id='{session}'")
        if not user:
            raise falcon.HTTPBadRequest('Could not validate session')
        self._validate_user_session(user['user_id'])
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
        users = {}
        for u in users_groups:
            user = self.db.fetchone_query(f"SELECT * FROM users WHERE user_id='{u['user_id']}'")
            # users['user_id'] = user['nickname']
            users[user['user_id']] = user['nickname']

        trans = self._get_transactions(group_id)

        trans_list: List[Transaction] = []
        for t in trans:
            trans_list.append(Transaction(t['user_pay'], str(t['users_paid']).split(','), t['amount']))

        debts: List[Debt] = transactions_to_debt(trans_list)
        debts_json = []
        for d in debts:
            if d.amount > 0:
                debts_json.append(
                    {
                        'from': d.sender,
                        'to': d.receiver,
                        'amount': d.amount
                    }
                )

        group_info = {
            'group_name': group['name'],
            'users': users,
            'transactions': trans,
            'debts': debts_json
        }

        return group_info

    def get_transaction_info(self, session: str, trans_id: str):
        user = self._get_user_from_database(session)
        trans = self.db.fetchone_query(f"SELECT * FROM transactions WHERE trans_id='{trans_id}'")
        self._validate_user_in_group(user['user_id'], trans['group_id'])

        paid_ids = trans['users_paid'].split(',')
        paid = []
        for p in paid_ids:
            paid.append(self._get_user_by_id(p)['nickname'])

        trans_info = {
            'payer': self._get_user_by_id(trans['user_pay'])['nickname'],
            'amount': trans['amount'],
            'description': trans['description'],
            'paid': paid,
        }

        return trans_info

    def _get_transactions(self, group_id: str):
        return self.db.fetchall_query(f"SELECT * FROM transactions WHERE group_id='{group_id}'")

    def _get_user_from_database(self, session: str):
        user = self.db.fetchone_query(f"SELECT * FROM users WHERE session_id='{session}'")
        if not user:
            raise falcon.HTTPBadRequest('Could not validate session')
        self._validate_user_session(user['user_id'])
        return user

    def _get_user_by_id(self, user_id: str):
        user = self.db.fetchone_query(f"SELECT * FROM users WHERE user_id='{user_id}'")
        if not user:
            raise falcon.HTTPBadRequest('Could not locate user.')
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

    def _validate_group_exists(self, group_id: str):
        group = self.db.fetchone_query(f"SELECT * FROM groups WHERE group_id = '{group_id}'")
        if group:
            return True
        else:
            return False

    def _validate_user_in_group(self, user_id: str, group_id: str):
        test = self.db.fetchone_query(f"SELECT * FROM users_groups WHERE user_id='{user_id}' AND group_id='{group_id}'")
        if test:
            return True
        else:
            return False
