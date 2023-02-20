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

@app.get("/data")
async def data():
    t = []
    x = []
    y = []
    z = []
    offset = time() - initial_time
    for a in range(1000):
        a *= 0.01
        a += offset
        t.append(a)
        w = 1
        x.append(sin(a*w))
        y.append(sin(a*w+1.4))
        z.append(sin(a*w+2.5))

    return [t,x,y,z]
    
@app.get("/log")
async def log():
    # This isn't actual data, we just need it to test the javascript
    data = "1,2,3,4\n"
    return  Response(content=data, media_type="text/plain")
