from fastapi import FastAPI, Response
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

async def wave_generator():
    w = 0.01
    amp = 1000
    w2 = 0.00001
    amp2 = 10000
    i = 0
    inc = 10
    while True:
        await asyncio.sleep(0.1)
        chunk = [(i,
            int(amp2*sin(i*w2)*sin(i*w)),
            int(amp*sin(i*w+1.4)),
            int(amp*sin(i*w+2.5)))
            for i in range(i, i+inc) ]
        data = {"axes":["t","x","y","z"],"data":chunk}
        i += inc
        yield json.dumps(data)

@app.get("/stream")
async def stream():
    return StreamingResponse(wave_generator())
            
    
@app.get("/log.csv")
async def log():
    # This isn't actual data, we just need it to test the javascript
    data = "1,2,3,4\n"
    return  Response(content=data, media_type="stream/octet")
