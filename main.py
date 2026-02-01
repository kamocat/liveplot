from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
import asyncio
import sensor
import os


server = FastAPI()

@server.get("/")
async def root(request: Request):
    return FileResponse(path="static/plot.html", media_type="text/html")

logdir = 'log/'
delimiter = ',\t'
server.mount("/static", StaticFiles(directory="static"), name="static")
server.mount("/log", StaticFiles(directory=logdir), name="log")


@server.get("/header")
async def header():
    scales = {"time": {"time": False}} #Treat as integers rather than timestamps
    n = set([x['scale'] for x in sensor.legend]) #Remove duplicate scales
    n.remove("time")
    for x in n:
        scales[x] = {"auto": True}
    data = {'series':sensor.legend, 'scales':scales}
    return JSONResponse(data)

@server.websocket("/stream")
async def stream(websocket: WebSocket):
    await websocket.accept()
    try:
        for vals in sensor.Sensor():
            chunk = [ [x] for x in vals ]
            await websocket.send_json(chunk)
    except WebSocketDisconnect:
        print('Client disconnected')
fname = None
file = None

def make_log():
    global fname
    global file
    files = os.listdir(logdir)
    files = [x.partition('.')[0] for x in files]
    files = [int(x) for x in files if x.isdigit()]
    files.append(0)
    highest = max(files)
    fname = f'{highest+1:03d}.txt'
    if file is not None:
        file.close()
    try:
        file = open(logdir+fname, 'w')
    except OSError as e:
        print(e)
        file = None
        fname = None
        return
    h = [x["label"] for x in sensor.legend]
    file.write(delimiter.join(h)+'\n')
    file.flush()

make_log()

@server.get("/logs")
async def list_logs(new: bool=False):
    if new:
        make_log()
    files = os.listdir(logdir)
    li = [f'<li><a href="/log/{f}" download>{f}</a> - {os.stat(logdir+f)[6]/1024:0.1f} kB</li>' for f in files]
    if fname is not None:
        li.insert(0,f'<li><a href="/log/{fname}" download>Latest</a></li>')
    else:
        li.insert(0,'<h3 style="color:red">Logging disabled until reboot</h3>')
    return HTMLResponse("\n".join(li))

