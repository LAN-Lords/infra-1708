from pydantic import BaseModel
from datetime import datetime


class Devices(BaseModel):
    id: str
    name: str
    layers: int
    ip: str
    mac: str
    status: bool
    #Created_At: datetime

    class Config:
        orm_mode = True


class NewConnections(BaseModel):
    id: str
    src_device_id: str
    dst_device_id: str

    class Config:
        orm_mode = True
