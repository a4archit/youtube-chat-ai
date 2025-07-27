

## dependencies
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from typing import Dict, Optional
from ychatai import YouTubeVideoChatAI



# creating app instance
app = FastAPI()



# ------------------------------------------------- API: Paths ---------------------------------------- #



@app.get('/')
def general_hit() -> JSONResponse:
    """ It returns the all possible paths """
    content = {
        'message': 'Welcome in Y-Chat AI, a tool by the help of this anyone can chat with the YouTube videos.',
        'possible paths': {
            '/status': 'to check the API properly processing',
            '/ready': 'to check model is ready to process queries',
            '/video': 'used to send video id to backend',
            '/query': 'used to ask query from related video',
            '/docs': 'original documentation'
        }
    }

    return JSONResponse(status_code=200, content=content)






@app.get(path='/status', name='Status checker', description='call to check the status of API')
def check_status() -> JSONResponse:
    """ It will return information about the status of """
    response = JSONResponse(content = {
        'status': 'ok',
        'status code': 200
    })

    return response





@app.get(path='/ready', name='Chat mode ready or not', description="This path is used to check is backend model is ready for quering or not.")
def ready() -> JSONResponse:
    """ Used to check is model ready for querying or not """
    try:
        model_preprocessed = True if youtube_chat_ai != None else False
    except:
        model_preprocessed = False 

    response = JSONResponse(content={
        'model status': model_preprocessed
    })

    return response





@app.get('/video')
def create_instance(id: Optional[str] = None):
    if id == "" or id is None:
        return HTTPException(status_code=422, detail="id not provided")
    
    global youtube_chat_ai

    try:
        youtube_chat_ai = YouTubeVideoChatAI(video_id=id)
    except Exception as e:
        details = {
            'message':'Something went wrong! Ping backend development team.',
            'error': e
        }
        return HTTPException(status_code=400, detail=details)

    content = {
        'status': 'ok',
        'msg': 'video processed successfully, now you can start quering'
    }
    return JSONResponse(status_code=200, content=content)



@app.get('/query')
def query(q: str = None):

    if q == "" or q is None:
        return HTTPException(status_code=422, detail='provide query(q) while hitting this api')
    
    try:
        response = youtube_chat_ai.invoke(query = q)
    except NameError:
        return HTTPException(status_code=400, detail={'error':'call /check api for preventing this issue.'})

    content = {
        'status': 'ok',
        'query': q,
        'ai response': response
    }

    return JSONResponse(status_code=200, content=content)










