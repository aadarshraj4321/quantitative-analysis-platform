FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git redis-server

COPY backend/requirements.txt .
COPY ml_models ./ml_models

RUN pip install --no-cache-dir -r requirements.txt

COPY backend .

COPY startup.sh .
RUN chmod +x startup.sh

EXPOSE 7860

CMD ["./startup.sh"]