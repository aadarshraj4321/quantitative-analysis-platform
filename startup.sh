# #!/bin/bash

# # Start the Redis server in the background
# redis-server --daemonize yes

# # Start the Celery worker in the background
# # We point it to the app folder where the code lives
# celery -A celery_worker.celery worker --loglevel=info &

# # Start the FastAPI server in the foreground
# # This is the main process that keeps the container alive
# # It must listen on 0.0.0.0 and port 7860 for Hugging Face Spaces
# uvicorn main:app --host 0.0.0.0 --port 7860


#!/bin/bash

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