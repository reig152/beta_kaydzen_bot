from enum import Enum
from urllib.parse import urlparse

from app.config import env


class RunningMode(str, Enum):
    LONG_POLLING = "LONG_POLLING"
    WEBHOOK = "WEBHOOK"


TG_TOKEN = env("TG_TOKEN", cast=str)

RUNNING_MODE = env("RUNNING_MODE", cast=RunningMode, default=RunningMode.LONG_POLLING)
WEBHOOK_URL = env("WEBHOOK_URL", cast=str, default="")

# Redis
REDIS_URL = env("REDIS_URL", cast=str, default="redis://localhost:6379")

# REDIS AUTH
PARSED_URL = urlparse(REDIS_URL)
REDIS_HOST = PARSED_URL.hostname
REDIS_PASS = PARSED_URL.password
