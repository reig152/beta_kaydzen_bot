#!/bin/sh

# Apply database migrations
echo "Applying database migrations ..."
python manage.py migrate

# Create superuser
echo "Creating superuser ..."
python manage.py createsuperuser --noinput

# Start server
echo "Starting server ..."
python -m uvicorn app.delivery.web.asgi:application --host 0.0.0.0 --port 8000

# Start bot
echo "Starting bot ..."
python -m app.delivery.bot
