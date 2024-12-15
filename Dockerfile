FROM python:3.13-slim-bookworm

WORKDIR /chatapp

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app

ENV DJANGO_SETTINGS_MODULE=chats.settings

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["daphne", "-u", "/tmp/daphne.sock", "chats.asgi:application"]