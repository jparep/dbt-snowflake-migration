FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.migration.txt .
RUN pip install --no-cache-dir -r requirements.migration.txt

# Copy migration script and utilities
COPY . .

# Set the default command to run the migration script
CMD ["python", "migration_script.py"]
