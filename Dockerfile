FROM python:3.13-slim-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app

ENV DJANGO_SETTINGS_MODULE=chats.settings

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["daphne ","-b 0.0.0.0" ,"-p 8000" ,"chats.asgi:application"]