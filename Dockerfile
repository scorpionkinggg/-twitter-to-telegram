FROM python:3.11-slim

# Install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Manually update CA certificates
RUN update-ca-certificates

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Fix for certifi CA location
ENV SSL_CERT_FILE=$(python -m certifi)

# Start the bot
CMD ["python", "main.py"]
