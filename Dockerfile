FROM python:3.11-slim

# Ensure SSL certs and system dependencies are installed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN update-ca-certificates

# Set working directory
WORKDIR /app

# Copy all files into container
COPY . .

# Install Python deps
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Force Python to use proper cert path
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

# Start script
CMD ["python", "main.py"]
