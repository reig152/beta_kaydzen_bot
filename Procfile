release: python manage.py migrate --noinput
web: python -m gunicorn app.delivery.web.asgi:application --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind :$PORT
worker: python -m app.delivery.bot --access-logfile $ACCESS_LOGFILE --error-logfile $ERROR_LOGFILE
# worker: python -m gunicorn app.delivery.bot:run_webhook --bind 0.0.0.0:8000 --worker-class aiohttp.GunicornWebWorker