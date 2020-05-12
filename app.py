from pathlib import Path
from argparse import ArgumentParser

from general_falcon_webserver import WebApp, SqliteDatabase

from backend.database_manager import DatabaseManager
from backend.endpoints.google_oauth import GoogleOauth
from backend.endpoints.groups import Groups
from backend.endpoints.transactions import Transactions
from backend.endpoints.users import Users


def parse_args():
    parser = ArgumentParser(description="Dank Bank v2")
    # Parse args for port in case system cannot serve on port 80
    parser.add_argument("--port", type=int, default=80, help="Port to host server.")
    parsed_args = parser.parse_args()
    return parsed_args


def configure_app():
    # Create WebApp
    app = WebApp('frontend', 'page404.html')

    # Create and set up database
    with open(Path('backend') / 'database_setup.sql') as file:
        db_config = file.read()
    db = SqliteDatabase('dank_bank_v2', db_config)
    # Apply database to a custom manager
    manager = DatabaseManager(db)

    # Add google oauth routing
    g_oauth = GoogleOauth(manager)
    app.add_route('g-oauth', g_oauth)

    users = Users(manager)
    app.add_route('users', users)

    groups = Groups(manager)
    app.add_route('groups', groups)

    trans = Transactions(manager)
    app.add_route('transactions', trans)

    return app


if __name__ == '__main__':
    args = parse_args()
    app = configure_app()
    app.launch_webserver(port=args.port)
