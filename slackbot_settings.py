import os
from os.path import dirname, join

from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

API_TOKEN = os.environ.get("API_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

DEFAULT_REPLY = "わかんない"

PLUGINS = ["plugins"]
