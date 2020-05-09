import json
import falcon

from backend.backend_utils import validate_params
from backend.database_manager import DatabaseManager


class Transactions:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def on_post(self, req, resp):
        if not validate_params(req.params, 'session', 'group_id', ):
            raise falcon.HTTPBadRequest("transactions post requires 'session', 'group_id', 'amount', 'paid' parameters")

        session = req.params['session']
        group_id = req.params['group_id']
        amount = float(req.params['amount'])
        paid = req.params['paid']
        desc = req.params['description']

        self.db.create_transaction(session, group_id, amount, paid, desc)
