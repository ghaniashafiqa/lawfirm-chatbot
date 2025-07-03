FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend app
COPY . .

# Expose port
EXPOSE 5000

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
