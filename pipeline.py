import subprocess

print("start processing the video")

subprocess.run(['python', 'video_procees.py'])

print('start extrecting the data from frame by Easy OCR')

subprocess.run(['python', 'ocr.py'])
