FROM python:3.11

WORKDIR /app

# ✅ Install root SSL certs explicitly
RUN apt-get update && \
    apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    && update-ca-certificates

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
