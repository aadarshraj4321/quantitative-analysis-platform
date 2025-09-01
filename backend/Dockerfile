FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get install -y git

COPY ./backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./ml_models /code/sentiment_model

WORKDIR /code/app