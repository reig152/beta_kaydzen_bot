release: python manage.py migrate --noinput
web: python -m gunicorn app.delivery.web.asgi:application --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
bot: python -m app.delivery.bot
