import json
import falcon

from backend.backend_utils import validate_params
from backend.database_manager import DatabaseManager


class Groups:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def on_get(self, req, resp):
        if not validate_params(req.params, 'session', 'group_id'):
            raise falcon.HTTPBadRequest("groups get requires 'session' and 'group_id' parameters")

        session = req.params['session'].replace("'", "").replace('"', '')
        group_id = req.params['group_id'].replace("'", "").replace('"', '')
        resp.body = json.dumps(self.db.get_group_info(session, group_id), ensure_ascii=True)

    def on_post(self, req, resp):
        if not validate_params(req.params, 'session', 'group_name'):
            raise falcon.HTTPBadRequest("groups post requires 'session' and 'group_name' parameters")

        session = req.params['session'].replace("'", "").replace('"', '')
        name = req.params['group_name'].replace("'", "").replace('"', '')
        resp.body = self.db.create_new_group(session, name)

    def on_put(self, req, resp):
        if not validate_params(req.params, 'session', 'group_id'):
            raise falcon.HTTPBadRequest("groups post requires 'session' and 'group_id' parameters")

        session = req.params['session'].replace("'", "").replace('"', '')
        group_id = req.params['group_id'].replace("'", "").replace('"', '')
        self.db.add_user_to_group(session, group_id)

    def on_delete(self, req, resp):
        if not validate_params(req.params, 'session', 'group_id'):
            raise falcon.HTTPBadRequest("groups post requires 'session' and 'group_id' parameters")

        session = req.params['session'].replace("'", "").replace('"', '')
        group_id = req.params['group_id'].replace("'", "").replace('"', '')
        self.db.delete_group(session, group_id)
