from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from math import sin, floor
from time import time

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/data")
async def data():
    t = []
    x = []
    y = []
    z = []
    offset = floor(time() * 100)
    for a in range(1000):
        a += offset
        t.append(a*10)
        w = 0.01
        x.append(sin(a*w))
        y.append(sin(a*w+1.4))
        z.append(sin(a*w+2.5))

    return [t,x,y,z]
    

