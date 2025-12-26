import os
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# ======================
# API SETTINGS
# ======================
API_DEBUG = True

UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ======================
# REDIS SETTINGS
# ======================
REDIS_QUEUE = "service_queue"
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# The tests and services expect REDIS_DB (not REDIS_DB_ID)
REDIS_DB = int(os.getenv("REDIS_DB", 0))

REDIS_HOST = os.getenv("REDIS_HOST", "redis")

API_SLEEP = 0.05

# ======================
# DATABASE SETTINGS
# ======================
DATABASE_USERNAME = os.getenv("POSTGRES_USER")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("POSTGRES_DB")

# ======================
# SECURITY
# ======================
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "S09WWHXB AJDIUEREHCN3752346572452VGGGVWWW526194",
)
