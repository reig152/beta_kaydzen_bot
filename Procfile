release: python manage.py migrate --noinput
# web: python -m gunicorn app.delivery.web.asgi:application --worker-class uvicorn.workers.UvicornWorker --bind :$PORT --workers $WORKERS --log-level $LOG_LEVEL --access-logfile $ACCESS_LOGFILE --error-logfile $ERROR_LOGFILE
web: gunicorn --bind :$PORT --workers 2 --worker-class uvicorn.workers.UvicornWorker app.delivery.web.asgi:application
bot: python -m app.delivery.bot
