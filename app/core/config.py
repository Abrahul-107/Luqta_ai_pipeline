import os
from dotenv import load_dotenv

load_dotenv()

required_vars = ["DB_NAME", "DB_USER", "DB_PASS", "DB_HOST", "DB_PORT"]
missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    raise EnvironmentError(f"❌ Missing required env vars: {', '.join(missing_vars)}")

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}
