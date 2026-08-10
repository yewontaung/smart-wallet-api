import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")
SHOW_SQL = os.getenv("SHOW_SQL", True)
JWT_SECRET = os.getenv("JWT_SECRET", "")
API_VERSION = os.getenv("API_VERSION")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD")