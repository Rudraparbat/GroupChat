#!/bin/sh

./wait-for-it.sh db:5432 --timeout=30 --strict -- echo "Database is up!"

echo "Running makemigrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate


echo "Starting Django development server..."
python daphne -b 0.0.0.0 -p 8000 chats.asgi:application


exec "$@"
