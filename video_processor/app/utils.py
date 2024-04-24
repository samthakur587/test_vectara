# SET CONFIG
import os
import re
from datetime import datetime
from pytube import YouTube
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
import sys

# Get the video URL from the command-line arguments
video_url = sys.argv[1]

# Your video processing code here
output_video_path = f"video_data/"
def download_video(url, output_path):
    """
    Download a video from a given url and save it to the output path.

    Parameters:
    url (str): The url of the video to download.
    output_path (str): The path to save the video to.

    Returns:
    dict: A dictionary containing the metadata of the video.
    """

    yt = YouTube(url)
    metadata = {"Author": yt.author, "Title": yt.title, "Views": yt.views}
    pattern = r'[^\w\s]'
    modified_string = re.sub(pattern, '_', yt.title)
    yt.streams.get_highest_resolution().download(
        output_path=output_path + f"/{yt.author}/", filename=f"input_vid_{modified_string}.mp4"
    )
    return metadata,modified_string

def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")

output_folder = "mixed_data/"
create_folder(output_folder)
metadata_vid,modified_string = download_video(video_url, output_video_path)
output_frame_folder = f"mixed_data/frames_{metadata_vid['Author']}/{modified_string}/"
create_folder(output_frame_folder)
audio_folder = f"mixed_data/output_{metadata_vid['Author']}/"
create_folder(audio_folder)
output_audio_path = f"mixed_data/output_{metadata_vid['Author']}/{modified_string}_audio.wav"
metadata_vid["Title"] = modified_string
filepath = output_video_path + f"/{metadata_vid['Author']}/" + f"input_vid_{modified_string}.mp4"

       
import json
# Step 1: Read the JSON file
with open('data.json', 'r') as file:
    data = json.load(file)
current_title = []
for t in data:
    current_title.append(t['Title']) 
if modified_string not in current_title:
    data.append(metadata_vid)

with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)
