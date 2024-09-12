from fastapi import FastAPI
from typing_extensions import List

from routers.network import fetch_network_data
from routers.netflow import fetch_netflow_data
from routers.syslog import fetch_syslog_data
import sys
from schemas import EventData, SysLogData

print(sys.path)
print("Python executable:", sys.executable)

app = FastAPI()


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
        system=row[4],
        number=row[5],
        config_type=row[6],
        description=row[7],
    ) for row in events]


@app.get("/netflow", response_model=List[EventData])
def get_netflow():
    events = fetch_netflow_data()  # Assuming this function fetches data from a database
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
