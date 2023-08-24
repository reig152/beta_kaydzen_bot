release: python manage.py migrate --noinput
logs: mkdir -p /app/logs && touch /app/logs/access.log /app/logs/error.log
web: python -m gunicorn app.delivery.web.asgi:application --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind :$PORT
bot: python -m app.delivery.bot --loglevel=INFO