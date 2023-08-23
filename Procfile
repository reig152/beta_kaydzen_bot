release: python manage.py migrate --noinput
web: python -m gunicorn app.delivery.web.asgi:application --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind :$PORT --log-level INFO --access-logfile /log/access.log 
bot: python -m app.delivery.bot