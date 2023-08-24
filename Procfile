release: python manage.py migrate --noinput
web: python -m gunicorn app.delivery.web.asgi:application --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind :$PORT --log-level INFO --access-logfile $ACCESS_LOGFILE --error-logfile $ERROR_LOGFILE
bot: python -m app.delivery.bot --loglevel INFO --access-logfile $ACCESS_LOGFILE --error-logfile $ERROR_LOGFILE
