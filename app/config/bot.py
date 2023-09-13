from enum import Enum
from urllib.parse import urlparse

from app.config import env


class RunningMode(str, Enum):
    LONG_POLLING = "LONG_POLLING"
    WEBHOOK = "WEBHOOK"


TG_TOKEN = env("TG_TOKEN", cast=str)
WEB_SERVER_HOST = env("WEB_SERVER_HOST", cast=str)
WEB_SERVER_PORT = env("WEB_SERVER_PORT")
WEBHOOK_PATH = env("WEBHOOK_PATH", cast=str)
BASE_WEBHOOK_URL = env("BASE_WEBHOOK_URL", cast=str)


RUNNING_MODE = env("RUNNING_MODE", cast=RunningMode, default=RunningMode.LONG_POLLING)
WEBHOOK_URL = env("WEBHOOK_URL", cast=str, default="")
