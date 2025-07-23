FROM python:3.11-slim

# Install system certificates and curl dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    && apt-get clean

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code
COPY . /app
WORKDIR /app

CMD ["python", "main.py"]
