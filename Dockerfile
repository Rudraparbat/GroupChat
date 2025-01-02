FROM python:3.13-slim-bookworm

RUN apt-get update 
# Set the working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . /app

# Ensure entrypoint.sh is executable
RUN chmod +x /app/entrypoint.sh

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=chats.settings
ENV PYTHONUNBUFFERED=1

# Expose the application port
EXPOSE 8000

# Start the application using entrypoint.sh
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

# Optional: You can set a CMD as fallback (e.g., to start Daphne or Django server)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
