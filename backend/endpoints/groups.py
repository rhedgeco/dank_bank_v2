import json
import falcon

from backend.backend_utils import validate_params
from backend.database_manager import DatabaseManager


class Groups:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def on_get(self, req, resp):
        if not validate_params(req.params, 'session', 'id'):
            raise falcon.HTTPBadRequest("groups get requires 'session' and 'id' parameters")

        session = req.params['session']
        id = req.params['id']
        resp.body = json.dumps(self.db.get_group_info(session, id), ensure_ascii=True)

    def on_post(self, req, resp):
        if not validate_params(req.params, 'session', 'group_name'):
            raise falcon.HTTPBadRequest("groups post requires 'session' and 'group_name' parameters")

        session = req.params['session']
        name = req.params['group_name']
        self.db.create_new_group(session, name)
