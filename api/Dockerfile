FROM python:3.10-alpine

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/app

COPY requirements.txt .

RUN apk update && apk add --no-cache bash \
    && apk add --no-cache curl \
    && apk add --no-cache ffmpeg \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "main.py"]
