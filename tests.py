import datetime
import uuid
import pytest
import os

from datetime import datetime as dt
from falcon import testing
from pathlib import Path

from general_falcon_webserver.backend.general_manager.databases import SqliteDatabase
from app import configure_app
from backend.database_manager import TIME_FORMAT


class User:
    def __init__(self, name: str):
        self.name: str = name
        self.id: str = uuid.uuid4().hex
        self.session_id: str = uuid.uuid4().hex
        self.session_timeout: str = (dt.now() + datetime.timedelta(0, 99999)).strftime(TIME_FORMAT)
        self.photo: str = 'none'


class Group:
    def __init__(self, name: str):
        self.name: str = name
        self.id: str = uuid.uuid4().hex


def delete_database():
    print('removing sqlite database...')
    sqlite_db = Path('general_falcon_webserver') / 'backend' / 'general_manager' / 'sqlite' / 'dank_bank_v2.db'
    if sqlite_db.exists():
        os.remove(sqlite_db)
    assert not sqlite_db.exists()
    print('database removed.')


delete_database()
app = configure_app()
db = SqliteDatabase('dank_bank_v2')

# base database testing setup
users = [
    User('Ryan Hedgecock'),
    User('Jeevanesh Lota'),
    User('Danny Giap'),
    User('Malaak Khalil')
]

for u in users:
    db.send_query(f"INSERT INTO users(user_id, nickname, session_id, session_timeout, photo) "
                  f"VALUES('{u.id}', '{u.name}', '{u.session_id}', '{u.session_timeout}', '{u.photo}')")


@pytest.fixture()
def client():
    return testing.TestClient(app.get_api_for_testing())


def test_get_user_info(client):
    res = client.simulate_get('/api/users', params={'session': users[0].session_id})
    assert res.status == '200 OK'

    info = {
        "id": users[0].id,
        "nickname": users[0].name,
        "photo": users[0].photo,
        "groups": []
    }

    assert res.json == info


def test_create_group(client):
    res = client.simulate_post('/api/groups', params={'session': users[0].session_id, 'group_name': 'Kool Kids'})
    assert res.status == '200 OK'


def get_main_group_id():
    user = client.simulate_get('/api/users', params={'session': users[0].session_id})
    assert user.status == '200 OK'
    return next(iter(user.json['groups'][0]))


def test_add_users_to_group(client):
    user = client.simulate_get('/api/users', params={'session': users[0].session_id})
    assert user.status == '200 OK'
    group_id = next(iter(user.json['groups'][0]))

    # test with user1
    res = client.simulate_put('/api/groups', params={'session': users[1].session_id, 'group_id': group_id})
    assert res.status == '200 OK'
    user = client.simulate_get('/api/users', params={'session': users[1].session_id})
    assert next(iter(user.json['groups'][0])) == group_id

    # test with user2
    res = client.simulate_put('/api/groups', params={'session': users[2].session_id, 'group_id': group_id})
    assert res.status == '200 OK'
    user = client.simulate_get('/api/users', params={'session': users[2].session_id})
    assert next(iter(user.json['groups'][0])) == group_id

    # test with user3
    res = client.simulate_put('/api/groups', params={'session': users[3].session_id, 'group_id': group_id})
    assert res.status == '200 OK'
    user = client.simulate_get('/api/users', params={'session': users[3].session_id})
    assert next(iter(user.json['groups'][0])) == group_id


def test_add_transactions(client):
    user = client.simulate_get('/api/users', params={'session': users[0].session_id})
    assert user.status == '200 OK'
    group_id = next(iter(user.json['groups'][0]))

    res = client.simulate_post('/api/transactions', params={
        'session': users[0].session_id,
        'group_id': group_id,
        'amount': 120.0,
        'paid': f'{users[1].id},{users[2].id},{users[3].id}',
        'description': 'Fancy Lunch'
    })
    assert res.status == '200 OK'

    res = client.simulate_post('/api/transactions', params={
        'session': users[1].session_id,
        'group_id': group_id,
        'amount': 60.0,
        'paid': f'{users[0].id},{users[2].id},{users[3].id}',
        'description': 'Takeout'
    })
    assert res.status == '200 OK'

    res = client.simulate_post('/api/transactions', params={
        'session': users[0].session_id,
        'group_id': group_id,
        'amount': 400.0,
        'paid': f'{users[1].id},{users[2].id},{users[3].id}',
        'description': 'Wind Surfing'
    })
    assert res.status == '200 OK'

    res = client.simulate_post('/api/transactions', params={
        'session': users[3].session_id,
        'group_id': group_id,
        'amount': 20.0,
        'paid': f'{users[1].id},{users[2].id},{users[0].id}',
        'description': 'French Fries'
    })
    assert res.status == '200 OK'


def test_get_group_info(client):
    user = client.simulate_get('/api/users', params={'session': users[0].session_id})
    assert user.status == '200 OK'
    group_id = next(iter(user.json['groups'][0]))

    res = client.simulate_get('/api/groups', params={'session': users[0].session_id, 'group_id': group_id})
    assert res.status == '200 OK'

    assert res.json['debts'] == [
        {'amount': 150.0, 'from': users[2].id, 'to': users[0].id},
        {'amount': 130.0, 'from': users[3].id, 'to': users[0].id},
        {'amount': 90.0, 'from': users[1].id, 'to': users[0].id}
    ]


def test_get_transactions(client):
    user = client.simulate_get('/api/users', params={'session': users[0].session_id})
    assert user.status == '200 OK'
    group_id = next(iter(user.json['groups'][0]))
    group = client.simulate_get('/api/groups', params={'session': users[0].session_id, 'group_id': group_id})
    assert group.status == '200 OK'
    trans_id = group.json['transactions'][0]['trans_id']

    res = client.simulate_get('/api/transactions', params={'session': users[0].session_id, 'trans_id': trans_id})
    assert res.status == '200 OK'

