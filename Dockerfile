FROM python:3.11-slim

# Install CA certs and basic deps
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Start app
CMD ["python", "main.py"]
