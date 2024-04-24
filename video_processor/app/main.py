from fastapi import FastAPI
from app.tasks import process_video
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError
from app.tasks import upload_to_vectara
from fastapi.staticfiles import StaticFiles
import json
from celery import chain

from vectara_connect.chat import query_vectara

import os
from dotenv import load_dotenv


load_dotenv()

CLIENT_ID = os.environ.get('client-id', None)
CLIENT_SECRET = os.environ.get('client-secret', None)

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="add any string...")
app.mount("/app/static", StaticFiles(directory="app/static"), name="static")



oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    client_kwargs={
        'scope': 'email openid profile',
        'redirect_url': 'http://localhost:8000/auth'
    }
)

templates = Jinja2Templates(directory="app/templates")

class VideoProcessRequest(BaseModel):
    video_url: str



@app.get("/")
def index(request: Request):
    user = request.session.get('user')
    if user:
        return RedirectResponse('welcome')

    return templates.TemplateResponse(
        name="home.html",
        context={"request": request}
    )


@app.get('/welcome')
def welcome(request: Request):
    user = request.session.get('user')
    if not user:
        return RedirectResponse('/')
    return templates.TemplateResponse(
        name='welcome.html',
        context={'request': request, 'user': user}
    )


@app.get("/login")
async def login(request: Request):
    url = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, url)


@app.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return templates.TemplateResponse(
            name='error.html',
            context={'request': request, 'error': e.error}
        )
    user = token.get('userinfo')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse('welcome')



@app.get('/logout')
def logout(request: Request):
    request.session.pop('user')
    request.session.clear()
    return RedirectResponse('/')



@app.post("/process_video")
async def process_video_endpoint(request: VideoProcessRequest):
    # Chain the tasks
    task_chain = chain(process_video.s(request.video_url), upload_to_vectara.s())
    result = task_chain.delay()

    return {"task_id": result.id}


meta_data = None
@app.get("/task/{task_id}")
async def get_task_status(task_id: str, request:Request):

    task = process_video.AsyncResult(task_id)
    global meta_data
    meta_data = task.result
    return {"status": task.status, "result": task.result}

print(f"bhai meta_data bhi aa rha h yha se embadding start kr de {meta_data}")



@app.post("/query")
async def handle_query(ques: str):
    vectara_response = query_vectara(ques)
    # Forward the response as streaming objects
    output = []
    js = json.loads(vectara_response.text)
    for res in js['responseSet']:
        for tex in res['response']:
            output.append(tex['text'])
    return {"output":output}


