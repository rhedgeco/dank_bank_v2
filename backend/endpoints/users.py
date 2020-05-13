import json
import falcon

from backend.backend_utils import validate_params
from backend.database_manager import DatabaseManager


class Users:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def on_get(self, req, resp):
        if not validate_params(req.params, 'session'):
            raise falcon.HTTPBadRequest("users get requires 'session' parameter")

        session = req.params['session'].replace("'", "").replace('"', '')
        resp.body = json.dumps(self.db.get_user_info(session), ensure_ascii=True)
