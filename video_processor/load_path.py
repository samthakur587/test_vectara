import os
import json
with open('data.json', 'r') as file:
    data = json.load(file)
t = data[-1]
print(t)
base = "mixed_data"
print(os.listdir(base))
transcript = base+"/output_"+t["Author"]
print(os.listdir(transcript))