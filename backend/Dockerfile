# FROM python:3.11-slim

# WORKDIR /code

# RUN apt-get update && apt-get install -y git

# COPY ./backend/requirements.txt .
# RUN pip install --no-cache-dir --upgrade -r requirements.txt

# COPY ./ml_models /code/sentiment_model

# WORKDIR /code/app




# FROM python:3.11-slim

# WORKDIR /code

# RUN apt-get update && apt-get install -y git

# COPY ./backend/requirements.txt .
# RUN pip install --no-cache-dir --upgrade -r requirements.txt

# COPY ./ml_models /code/sentiment_model

# WORKDIR /code/app

# # This is the default command for our web server
# CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]






FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get install -y git

COPY ./backend/requirements.txt .
# Install Gunicorn for a production-ready server
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt

COPY ./ml_models /code/sentiment_model

# Copy the application code last. All code will live in /code now.
COPY ./backend .

# The default command is to start the web server.
# Render's free web services require port 10000.
CMD ["gunicorn", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:10000"]