release: python manage.py migrate --noinput
web: python -m gunicorn app.delivery.web.asgi:application --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --workers $WORKERS --log-level $LOG_LEVEL --access-logfile $ACCESS_LOGFILE --error-logfile $ERROR_LOGFILE
bot: python -m app.delivery.bot
