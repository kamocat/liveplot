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
        amp = 1000
        w2 = 0.00001
        amp2 = 10000
        data['x'].append(int(amp2*sin(a*w2)*sin(a*w)))
        data['y'].append(int(amp*sin(a*w+1.4)))
        data['z'].append(int(amp*sin(a*w+2.5)))
    return data
    
@app.get("/log.csv")
async def log():
    # This isn't actual data, we just need it to test the javascript
    data = "1,2,3,4\n"
    return  Response(content=data, media_type="stream/octet")
