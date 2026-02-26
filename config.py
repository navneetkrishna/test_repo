import os
from dotenv import load_dotenv

load_dotenv()

# --- API ---
BASE_URL = os.getenv("BASE_URL", "https://petstore.swagger.io/v2")
API_KEY  = os.getenv("API_KEY", "special-key")

# --- Resource URLs ---
PET_URL   = f"{BASE_URL}/pet"
STORE_URL = f"{BASE_URL}/store"
USER_URL  = f"{BASE_URL}/user"
