from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from math import sin

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
    for a in range(100):
        t.append(a*10)
        w = 0.1
        x.append(sin(a*w))
        y.append(sin(a*w+1.4))
        z.append(sin(a*w+3.1))

    return [t,x,y,z]
    

