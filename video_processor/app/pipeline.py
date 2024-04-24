import subprocess

print("Start processing the video")
subprocess.run(['python', 'app/utils.py', 'https://www.youtube.com/watch?v=wjZofJX0v4M'])

# Execute the 'video_process.py' script with an argument 'video_url'
subprocess.run(['python', 'app/video_procees.py', 'https://www.youtube.com/watch?v=wjZofJX0v4M'])

print('Start extracting the data from frames using Easy OCR')

# Execute the 'ocr.py' script
subprocess.run(['python', 'app/ocr.py'])
