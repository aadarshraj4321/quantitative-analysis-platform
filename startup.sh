#!/bin/sh

# Start the Redis server in the background WITH PERSISTENCE DISABLED
# The '--save ""' command tells Redis not to create any RDB snapshots.
redis-server --daemonize yes --save "" --appendonly no

echo "Redis started with persistence disabled."

# Start the Celery worker in the background
celery -A celery_worker.celery worker --loglevel=info &

echo "Celery worker started."

# Start the FastAPI server in the foreground
# This keeps the container alive.
echo "Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port 7860