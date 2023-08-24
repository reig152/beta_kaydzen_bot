release: python manage.py migrate --noinput
web: python -m gunicorn app.delivery.web.asgi:application --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind :$PORT
logs: mkdir -p /app/logs && touch $ACCESS_LOGFILE $ERROR_LOGFILE
bot: python -m app.delivery.bot --loglevel=INFO