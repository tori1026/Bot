FROM python:3.10.5-alpine3.16
WORKDIR /bot
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt