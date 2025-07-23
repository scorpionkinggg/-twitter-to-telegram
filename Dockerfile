FROM python:3.11

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy app files
COPY . .

# Install Python deps
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run your bot
CMD ["python", "main.py"]
