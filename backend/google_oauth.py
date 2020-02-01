import falcon
import cachecontrol
import google.auth.transport.requests
import requests

from backend.database_manager import DatabaseManager
from backend.backend_utils import validate_params

from google.oauth2 import id_token
from google.auth.transport import requests

CLIENT_ID = '67665061536-mh57v3d9uef3edep23kjmgeqlqrobb1b.apps.googleusercontent.com'


class GoogleOauth:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def on_post(self, req, resp):
        if not validate_params(req.params, 'idtoken'):
            raise falcon.HTTPBadRequest('oauth post requires \'idtoken\' parameter')

        token = req.params['idtoken']
        # example from https://developers.google.com/identity/sign-in/web/backend-auth
        try:
            session = requests.Request()
            cached_session = cachecontrol.CacheControl(session)
            request = google.auth.transport.requests.Request(session=cached_session)
            idinfo = id_token.verify_oauth2_token(token, request, CLIENT_ID)

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            userid = idinfo['sub']
            self.db.sign_in_or_create_oauth_user(userid)
        except ValueError:
            raise falcon.HTTPUnauthorized('Token not accepted')
            pass
