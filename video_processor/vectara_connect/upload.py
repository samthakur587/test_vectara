from dotenv import load_dotenv
import os

import requests
load_dotenv()

VECTARA_API_KEY = os.getenv('VECTARA_API_KEY')
VECTARA_CUSTOMER_ID = os.getenv('VECTARA_CUSTOMER_ID')
CORPUS_ID = os.getenv('CORPUS_ID')
def clean_llm(text):
    return text

def upload_file(file_path):
    url = f"https://api.vectara.io/v1/upload?c={VECTARA_CUSTOMER_ID}&o={CORPUS_ID}"

    headers = {
        'Accept': 'application/json',
        'x-api-key': VECTARA_API_KEY
    }
    count = 0
    for f in os.listdir(file_path):
        count +=1
        file_full_path = os.path.join(file_path, f)
        with open(file_full_path, "rb") as file:
            file_content = file.read()
        if count==2:
            file_content = clean_llm(file_content)
        files = [
            ('file', (f'file_{f}', file_content, 'application/octet-stream'))]
        response = requests.post(url, headers=headers, files=files)
    print(response.text)

    return response.text

if __name__ == "__main__":
    file_path = "./mixed_data/output_Sequoia Capital"
    upload_file(file_path)
