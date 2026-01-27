from fastapi import FastAPI, Response, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from math import sin, floor
from time import time
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
import json
import asyncio

initial_time = time()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    # Serve a static file
    return FileResponse(path="static/plot.html", media_type="text/html")

@app.websocket("/stream")
async def stream(websocket: WebSocket):
    await websocket.accept()
    w = 0.1
    amp = 1000
    w2 = 0.0001
    amp2 = 10000
    i = 0
    inc = 10
    try:
        while True:
            await asyncio.sleep(1)
            t = range(i, i+inc)
            chunk = [ list(t),
                [int(amp2*sin(i*w2)*sin(i*w)) for i in t],
                [int(amp*sin(i*w+1.4)) for i in t],
                [int(amp*sin(i*w+2.5)) for i in t],
                ]
            data = {"axes":["x","y","z"],"data":chunk}
            i += inc
            await websocket.send_json(chunk)
    except WebSocketDisconnect:
        return

@app.get("/log.csv")
async def log():
    # This isn't actual data, we just need it to test the javascript
    data = "1,2,3,4\n"
    return  Response(content=data, media_type="stream/octet")