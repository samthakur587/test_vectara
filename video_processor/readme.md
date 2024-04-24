# Video Processor

This is a video processing pipeline built using FastAPI, Celery, and Redis.

## Prerequisites

1. Python 3.12.3 (or a compatible version)
2. Redis server

## Setup

1. Create a new Python virtual environment and activate it.
2. Navigate to the `video_processor` directory.

## Install dependencies

1. Install the required packages for the `app` module:
   ```
   cd app/
   pip install -r requirements.txt
   ```
2. Install the required packages for the `worker` module:
   ```
   cd worker/
   pip install -r requirements.txt
   ```

## Install Redis

1. Install the Redis server:
   ```
   sudo apt install redis-server -y
   ```

## Run the application

1. Start the Redis server in a new terminal:
   ```
   sudo redis-server
   ```
2. Start the Celery worker in a new terminal:
   ```
   cd video_processor/
   celery -A worker.celery_worker.app worker --beat --loglevel=info --pool=solo
   ```
3. Start the FastAPI application in a new terminal:
   ```
   cd video_processor/
   uvicorn app.main:app --reload
   ```

 (PS. iF you are lazy like me, run ```sudo setup.sh```, this will start the servers and do the needful :) 

Now, the application should be running and ready to process videos.

## Usage

1. Send a POST request to `http://localhost:8000/process_video` with the video URL in the request body.
2. The response will contain the task ID.
3. You can check the status of the task by sending a GET request to `http://localhost:8000/task/{task_id}`.

The video processing pipeline consists of the following steps:

1. Download the video from the provided URL.
2. Convert the video to a sequence of images.
3. Convert the video to an audio file.
4. Perform speech recognition on the audio file and save the transcript.

The processed data, including the video metadata and the text transcript, will be saved in the appropriate directories.