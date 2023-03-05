from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from math import sin, floor
from time import time
from fastapi.responses import FileResponse

initial_time = time()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    # Serve a static file
    return FileResponse(path="static/plot.html", media_type="text/html")

@app.get("/data/{t0}")
async def data(t0:int):
    data = {"t0":t0, "period":0.01, "x":[], "y":[], "z":[]}
    for a in range(60):
        a += t0 
        w = 0.01
        amp = 15
        data['x'].append(round(amp*sin(a*w),3))
        data['y'].append(round(amp*sin(a*w+1.4),3))
        data['z'].append(round(amp*sin(a*w+2.5),3))
    return data
    
@app.get("/log.csv")
async def log():
    # This isn't actual data, we just need it to test the javascript
    data = "1,2,3,4\n"
    return  Response(content=data, media_type="stream/octet")
