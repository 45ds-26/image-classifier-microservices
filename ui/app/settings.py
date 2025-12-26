import os

API_HOST = os.getenv("API_HOST", "api")
API_PORT = os.getenv("API_PORT", "5000")

API_BASE_URL = f"http://{API_HOST}:{API_PORT}"
