# Dockerfile
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole app
COPY . .

# Expose the Flask port
EXPOSE 5000

# Default command
CMD ["python", "run.py"]
