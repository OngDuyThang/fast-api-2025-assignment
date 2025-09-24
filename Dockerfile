FROM python:3.11-slim

# Create and set working directory inside container
WORKDIR /app/app

# Install system dependencies (if needed, e.g. psycopg2 dependencies)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc tk \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the entire project
COPY . /app/

# Run Alembic migrations and then start the app
CMD alembic upgrade head && python run.py
