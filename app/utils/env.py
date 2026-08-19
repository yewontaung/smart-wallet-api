import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "")
SHOW_SQL = os.getenv("SHOW_SQL", True)
JWT_SECRET = os.getenv("JWT_SECRET", "")
ALGO = os.getenv("ALGO", "HS256")
API_VERSION = os.getenv("API_VERSION")
DEMO_PASSWORD = os.getenv("DEMO_PASSWORD")
DEMO_PIN = os.getenv("DEMO_PIN")
ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "")