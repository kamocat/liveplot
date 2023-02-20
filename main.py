from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from math import sin, floor
from time import time

initial_time = time()

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
    

