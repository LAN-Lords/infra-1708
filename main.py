
from fastapi import FastAPI
from routers.network import fetch_network_data
from routers.netflow import fetch_netflow_data
from routers.syslog import fetch_syslog_data
import sys

print(sys.path)
print("Python executable:", sys.executable)

app = FastAPI()

@app.get("/network")
def get_network():
    return fetch_network_data()

@app.get("/syslog")
def get_syslog():
    return fetch_syslog_data()

@app.get("/netflow")
def get_netflow():
    return get_netflow()