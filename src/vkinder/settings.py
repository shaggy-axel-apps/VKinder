import os

from dotenv import load_dotenv


load_dotenv()

V = os.environ.get("V", "")
GROUP_TOKEN = os.environ.get("GROUP_TOKEN", "")
USER_TOKEN = os.environ.get("USER_TOKEN", "")

DB_CREDS = {
    "USER": os.environ.get("POSTGRES_USER", "postgres"),
    "PASS": os.environ.get("POSTGRES_PASSWORD"),
    "NAME": os.environ.get("POSTGRES_DB"),
    "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
    "PORT": int(os.environ.get("POSTGRES_PORT", "5432"))
}


MIN_AGE = 18
MAX_AGE = 99
