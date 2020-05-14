import json
import falcon

from backend.backend_utils import validate_params
from backend.database_manager import DatabaseManager


class Transactions:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def on_get(self, req, resp):
        if not validate_params(req.params, 'session', 'trans_id'):
            raise falcon.HTTPBadRequest("transactions post requires 'session', and 'trans_id' parameters")

        session = req.params['session'].replace("'", "").replace('"', '')
        trans_id = req.params['trans_id'].replace("'", "").replace('"', '')
        resp.body = json.dumps(self.db.get_transaction_info(session, trans_id), ensure_ascii=True)

    def on_post(self, req, resp):
        if not validate_params(req.params, 'session', 'group_id', 'amount', 'paid', 'description'):
            raise falcon.HTTPBadRequest(
                "transactions post requires 'session', 'group_id', 'amount', 'paid', and 'description' parameters")

        session = req.params['session'].replace("'", "").replace('"', '')
        group_id = req.params['group_id'].replace("'", "").replace('"', '')
        amount = float(req.params['amount'].replace("'", "").replace('"', ''))
        paid = req.params['paid'].replace("'", "").replace('"', '')
        desc = req.params['description'].replace("'", "").replace('"', '')

        if amount > 0:
            self.db.create_transaction(session, group_id, amount, paid, desc)
