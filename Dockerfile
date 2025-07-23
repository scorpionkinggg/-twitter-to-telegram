FROM python:3.11-slim

# Install certificate authorities and essential tools
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set environment variable to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Ensure certificates are up to date
RUN update-ca-certificates

# Set working directory
WORKDIR /app

# Copy all project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Default command
CMD ["python", "main.py"]


