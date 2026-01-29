from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from math import sin, floor
from time import time
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import json
import asyncio
import os

initial_time = time()

app = FastAPI()

logdir = 'log'
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/log", StaticFiles(directory=logdir), name="log")

class Series(BaseModel):
    scale: str
    label: str
    def __init__(self, label: str, scale: str, **kwargs):
        super().__init__(label=label, scale=scale)

class ChartOpts(BaseModel):
    series: list[Series]
    scales: dict

@app.get("/header")
def header():
    plots = [
        Series("seconds", "time"),
        Series("X", "acceleration"),
        Series("RPM", "rotation"),
        Series("Upper", "temperature"),
    ]
    scales = {"time": {"time": False}}
    n = set([x.scale for x in plots])
    n.remove("time")
    for x in n:
        scales[x] = {"auto": True}
    data = ChartOpts(series=plots, scales=scales)
    return data

fname = "tmp.csv"
file = None

def make_log():
    global fname
    global file
    files = os.listdir(logdir)
    files = [os.path.splitext(x)[0] for x in files]
    files = [int(x) for x in files if x.isnumeric()]
    files.append(0)
    highest = max(files)
    fname = f'{highest+1:03d}.txt'
    if file is not None:
        file.close()
    file = open(os.path.join(logdir,fname), 'w')
    h = header().series
    h = [x.label for x in h]
    file.write(','.join(h)+'\n')
    file.flush()

make_log()

@app.get("/latest")
async def root(request: Request):
    return FileResponse(path=os.path.join(logdir,fname), media_type="text/csv")

@app.get("/")
async def root(request: Request):
    return FileResponse(path="static/plot.html", media_type="text/html")

@app.get("/logs")
async def list_logs(new: bool=False):
    if new:
        make_log()
    files = os.listdir(logdir)
    # Normally we would do this with templating, but porting jina2 to CircuitPython seems like overkill
    li = [f'<li><a href="/log/{f}">{f}</a> {os.path.getsize(os.path.join(logdir,f))/1024:0.1f} kB</li>' for f in files]
    li.insert(0,'<li><a href="/latest">Latest</a></li>')
    return HTMLResponse("\n".join(li))

@app.websocket("/stream")
async def stream(websocket: WebSocket):
    await websocket.accept()
    w = 0.1
    amp = 1000
    w2 = 0.001
    amp2 = 10000
    i = 0
    inc = 10
    try:
        while True:
            await asyncio.sleep(0.1)
            t = range(i, i + inc)
            chunk = [
                list(t),
                [int(amp2 * sin(i * w2) * sin(i * w)) for i in t],
                [int(amp * sin(i * w + 1.4)) for i in t],
                [int(amp * sin(i * w + 2.5)) for i in t],
            ]
            i += inc
            await websocket.send_json(chunk)
    except WebSocketDisconnect:
        return
