from fastapi import FastAPI, Response, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from math import sin, floor
from time import time
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
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


class Series(BaseModel):
    scale: str
    label: str

    def __init__(self, label: str, scale: str, **kwargs):
        super().__init__(label=label, scale=scale)


class ChartOpts(BaseModel):
    series: list[Series]
    scales: dict


@app.get("/header")
async def header():
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


@app.get("/log.csv")
async def log():
    # This isn't actual data, we just need it to test the javascript
    data = "1,2,3,4\n"
    return Response(content=data, media_type="stream/octet")
