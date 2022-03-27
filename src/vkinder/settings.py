import os

import sqlalchemy as sq
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

# ENVIRONMENT SETTINGS
load_dotenv()
V = 5.131
GROUP_TOKEN = os.environ.get("GROUP_TOKEN", "")
USER_TOKEN = os.environ.get("USER_TOKEN", "")

# DATABASE SETTINGS
DB_CREDS = {
    "USER": os.environ.get("POSTGRES_USER", "postgres"),
    "PASS": os.environ.get("POSTGRES_PASSWORD", "postgres"),
    "NAME": os.environ.get("POSTGRES_DB", "vkinder"),
    "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
    "PORT": int(os.environ.get("POSTGRES_PORT", "5432"))
}
engine = sq.create_engine(
    ('postgresql://'
     f'{DB_CREDS["USER"]}:{DB_CREDS["PASS"]}@'
     f'{DB_CREDS["HOST"]}:{DB_CREDS["PORT"]}/'
     f'{DB_CREDS["NAME"]}'),
    client_encoding='utf8'
)
Base = declarative_base()

# MANAGEMENT COMMANDS
START_COMMAND = "start"
MIGRATE_COMMAND = "migrate"

# SEARCHING SETTINGS
MALE = ("мальчик", "парень", "мужчина")
FEMALE = ("девочка", "девушка", "женщина")
START_SEARCH_WORDS = (*MALE, *FEMALE)
MIN_AGE = 18
MAX_AGE = 99

# MAIN BUTTONS
BUTTONS = [
    "Help", "Find Pair",
    "Favorites", "BlackList"
]