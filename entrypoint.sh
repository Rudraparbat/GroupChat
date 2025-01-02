#!/bin/sh

set -e  

if [ "$DJANGO_ENV" = "local" ]; then
  echo "Waiting for PostgreSQL..."
  /app/wait-for-it.sh db:5432 --timeout=30 --strict -- echo "Database is up!"
fi

echo "Running makemigrations..."
python manage.py makemigrations

echo "Applying migrations..."
python manage.py migrate


echo "Starting Django server..."

daphne -b 0.0.0.0 -p 8000 chats.asgi:application


exec "$@"
