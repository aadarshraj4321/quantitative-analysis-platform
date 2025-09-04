# This is the single Dockerfile for our entire backend on Hugging Face Spaces
FROM python:3.11-slim

# Set a single working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git redis-server

# Copy all requirements and model files first for better caching
COPY backend/requirements.txt .
COPY ml_models ./ml_models

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend source code
COPY backend .

# Create a startup script
COPY startup.sh .
RUN chmod +x startup.sh

# Expose the port FastAPI will run on
EXPOSE 7860

# The command to run our startup script
CMD ["./startup.sh"]