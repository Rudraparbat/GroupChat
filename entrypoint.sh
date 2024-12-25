#!/bin/sh

echo "Flushing Redis data..."
redis-cli FLUSHALL

echo "Running makemigrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate


echo "Starting Django server..."

daphne -b 0.0.0.0 -p 8000 chats.asgi:application


exec "$@"
