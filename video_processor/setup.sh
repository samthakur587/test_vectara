#!/bin/bash

# Set the Python version to use
PYTHON_VERSION="3.12.3"

# Create and activate the virtual environment
python3 -m venv env
source env/bin/activate

# Install dependencies
cd app/
pip install -r requirements.txt
cd ../worker/
pip install -r requirements.txt

# Install Redis
sudo apt install redis-server -y

# Start Redis server
echo "Starting Redis server..."
redis-server &

# Start Celery worker
echo "Starting Celery worker..."
cd ../
celery -A worker.celery_worker.app worker --beat --loglevel=info --pool=solo &

# Start FastAPI application
echo "Starting FastAPI application..."
uvicorn app.main:app --reload &

echo "Video Processor is now running."
echo "You can access the API at http://localhost:8000"

# Keep the script running to maintain the processes
while true; do
    sleep 1
done