from fastapi import FastAPI
from typing import List
from routers.network import fetch_network_data
from routers.netflow import fetch_netflow_data
from routers.syslog import fetch_syslog_data
import sys
from schemas import EventData, SysLogData
import socketio
import asyncio
import uvicorn  # <-- Add this import

# Debug info
print(sys.path)
print("Python executable:", sys.executable)

sio = socketio.AsyncServer(async_mode='asgi')
app = FastAPI()

app_sio = socketio.ASGIApp(sio, app)

@app.get("/")
def read_root():
    return {
        "status": "OK"
    }

@app.get("/network")
def get_network():
    return fetch_network_data()

@app.get("/syslog", response_model=List[SysLogData])
def get_syslog():
    events = fetch_syslog_data()
    return [SysLogData(
        id=row[0],
        timestamp1=row[1],
        timestamp2=row[2],
        ip_address=row[3],
        severity=row[5],
        message=f'{row[4]}-{row[6]}:{row[7]}'  # Adjust message formatting
    ) for row in events]

@app.get("/netflow", response_model=List[EventData])
def get_netflow():
    events = fetch_netflow_data()
    return [EventData(
        id=row[0],
        timestamp=row[1],
        event_type=row[2],
        action=row[3],
        protocol=row[4],
        src_ip=row[5],
        src_port=row[6],
        dst_ip=row[7],
        dst_port=row[8],
        x_src_ip=row[9],
        x_src_port=row[10],
        x_dst_ip=row[11],
        x_dst_port=row[12],
        in_bytes=row[13],
        out_bytes=row[14]
    ) for row in events]

@app.get("/netflow/{Ip}", response_model=List[EventData])
def get_netflow_by_ip(Ip: str):
    events = fetch_netflow_data()
    matching_events = [EventData(
        id=row[0],
        timestamp=row[1],
        event_type=row[2],
        action=row[3],
        protocol=row[4],
        src_ip=row[5],
        src_port=row[6],
        dst_ip=row[7],
        dst_port=row[8],
        x_src_ip=row[9],
        x_src_port=row[10],
        x_dst_ip=row[11],
        x_dst_port=row[12],
        in_bytes=row[13],
        out_bytes=row[14]
    ) for row in events if row[5] == Ip or row[7] == Ip]

    return matching_events

@sio.event
async def connect(sid, environ):
    print("New-Connection ", sid)
    await sio.emit("status", {"data": "Connected"})

@sio.event
async def disconnect(sid):
    print("Disconnected ", sid)

if __name__ == "__main__":
    uvicorn.run(app_sio, host="0.0.0.0", port=8000)
