FROM python:3.10-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set work directory
WORKDIR /app
# User
RUN addgroup app && adduser -S -G app app
RUN chown -R app:app /app

# Install system dependencies
RUN apk update && apk add --no-cache \
  mariadb-dev \
  build-base \
  python3-dev \
  py3-pip \
  mariadb-client \
  mariadb-connector-c-dev \
  gcc \
  bash

# Install pipenv
RUN pip install pipenv

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock /app/

# Install project dependencies
RUN pipenv install --deploy --system

# Copy project files to the working directory
COPY . .

# Ensure the entrypoint script is executable
RUN chown -R app:app /app
RUN chmod +x ./docker-entrypoint.sh

USER app
# Expose the port the app runs on
EXPOSE 8000