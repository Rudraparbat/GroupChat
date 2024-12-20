FROM python:3.13-slim-bookworm

# Set the working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . /app

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=chats.settings
ENV PYTHONUNBUFFERED=1

# Expose the application port
EXPOSE 8000

# Start the application using Daphne
ENTRYPOINT  ["./entrypoint.sh"]
