import dj_database_url

from app.config import env

# Postgresql
DATABASE_URL = env("DATABASE_URL", cast=str, default="sqlite:///db.sqlite3")
CONN_MAX_AGE = env("CONN_MAX_AGE", cast=int, default=600)

DATABASES = {
    "default": dj_database_url.parse(DATABASE_URL, conn_max_age=CONN_MAX_AGE),
}


DATABASE_URL = env("DATABASE_URL", cast=str, default="postgres://user:pass@localhost:5432/default_db")
