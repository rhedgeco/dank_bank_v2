from pathlib import Path

from general_falcon_webserver import WebApp, SqliteDatabase

from backend.database_manager import DatabaseManager
from backend.google_oauth import GoogleOauth

# Create WebApp
app = WebApp('frontend')

# Create and set up database
with open(Path('backend') / 'database_setup.sql') as file:
    db_config = file.read()
db = SqliteDatabase('dank_bank_v2', db_config)
# Apply database to a custom manager
manager = DatabaseManager(db)

# Add google oauth routing
g_oauth = GoogleOauth('frontend/oauth_page.html', manager)
app.add_route('g-oauth', g_oauth)

# Launch the webserver
app.launch_webserver()
