from dotenv import load_dotenv
import os
import json

# from fastapi import FastAPI, Response
import requests
load_dotenv()

VECTARA_API_KEY = os.getenv('VECTARA_API_KEY')
VECTARA_CUSTOMER_ID = os.getenv('VECTARA_CUSTOMER_ID')
CORPUS_ID = os.getenv('CORPUS_ID')

# app = FastAPI()

def query_vectara(ques: str):
    url = "https://api.vectara.io/v1/query"
    payload = {
        "query": [
            {
                "query": ques,
                "start": 0,
                "numResults": 3,
                "contextConfig": {
                    "sentences_before": 3,
                    "sentences_after": 3,
                    "start_tag": "<b>",
                    "end_tag": "</b>"
                },
                "corpusKey": [
                    {
                        "corpus_id": CORPUS_ID
                    }
                ],
                "summary": [
                    {
                        "max_summarized_results": 3,
                        "response_lang": "en"
                    }
                ]
            }
        ]
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'customer-id': VECTARA_CUSTOMER_ID,
        'x-api-key': VECTARA_API_KEY
    }

    response = requests.post(url, headers=headers, json=payload, stream=False)

    return response

# @app.post("/query")
# async def handle_query(ques: str):
#     vectara_response = query_vectara(ques)
#     # Forward the response as streaming objects
#     for chunk in vectara_response.iter_content(chunk_size=1024):
#         yield chunk

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

import json
if __name__ == "__main__":
    ans = query_vectara("future of rag agents").text
    js = json.loads(ans)
    for res in js['responseSet']:
        for tex in res['response']:
            print(tex['text'])
    