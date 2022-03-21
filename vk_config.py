import os

from dotenv import load_dotenv


load_dotenv()

V = os.environ.get("V", "")
GROUP_TOKEN = os.environ.get("GROUP_TOKEN", "")
USER_TOKEN = os.environ.get("USER_TOKEN", "")
