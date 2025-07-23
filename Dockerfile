FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libssl-dev \
    libffi-dev \
    curl \
    ca-certificates \
    && update-ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Force install latest certifi CA bundle
RUN python -m pip install certifi && \
    CERT_FILE=$(python -m certifi) && \
    export SSL_CERT_FILE=$CERT_FILE

# Start app
CMD ["python", "main.py"]
