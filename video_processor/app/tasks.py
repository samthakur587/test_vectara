from celery import Celery
import subprocess
import shutil
from vectara_connect.upload import upload_file
import json, os
#import subprocess
# from app.config import *
#from app.video_process import download_video, video_to_images, video_to_audio, audio_to_text
#from app.utils import create_folder, output_video_path, output_frame_folder, audio_folder
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND,  include=["app.tasks"])
# cele.config_from_object('config')


@app.task
def process_video(key:str,video_url:str):
    print("Start processing the video")
    subprocess.run(['python', 'app/utils.py', video_url])

    # Execute the 'video_process.py' script with an argument 'video_url'
    subprocess.run(['python', 'app/video_procees.py', video_url])

    print('Start extracting the data from frames using Easy OCR')

    # Execute the 'ocr.py' script
    #subprocess.run(['python', 'app/ocr.py'])
    with open('data.json', 'r') as file:
        data = json.load(file)
    base = os.getcwd() + "/"+"mixed_data"
    video_data = os.getcwd() + "/"+ "video_data"
    t = data[-1]
    transcript = base+"/output_"+t["Author"]+"/"+f"transcript_{t['Title']}_text.txt"
    with open(transcript,'r') as f:
        str_input = f.read()
    shutil.rmtree(base)
    shutil.rmtree(video_data)
    return str_input


# @app.task
# def upload_to_vectara(video_url):
#     with open('data.json', 'r') as file:
#         data = json.load(file)

#     t = data[-1]
#     print(t)
#     base = "mixed_data"
#     print(os.listdir(base))
#     transcript = base+"/output_"+t["Author"]
#     print(os.listdir(transcript))

#     #@samunder ye check karna lagta hai error hai...
#     print("Starting Uploading")
#     upload_file(transcript)
#     shutil.rmtree("mixed_data")
#     shutil.rmtree('video_data')
#     return "done"

app.tasks.register(process_video)
