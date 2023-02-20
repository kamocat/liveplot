from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from math import sin, floor
from time import time

initial_time = time()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    # Serve a static file
    with open("static/plot.html", encoding="utf-8") as f:
        return Response(content=f.read(), media_type="text/html")

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
    
@app.get("/log.csv")
async def log():
    # This isn't actual data, we just need it to test the javascript
    pass
