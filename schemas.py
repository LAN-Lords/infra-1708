from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from datetime import datetime


class EventData(BaseModel):
    id: int
    timestamp: datetime
    event_type: str
    action: str
    protocol: str
    src_ip: str
    src_port: int
    dst_ip: str
    dst_port: int
    x_src_ip: str
    x_src_port: int
    x_dst_ip: str
    x_dst_port: int
    in_bytes: int
    out_bytes: int


class SysLogData(BaseModel):
    id: int
    timestamp1: datetime
    timestamp2: datetime
    ip_address: str
    # system: str
    severity: str
    message: str
    # config_type: str
    # description: str


class Connection(BaseModel):
    id: int
    src_ip: str
    dst_ip: str


class NetworkSchema(BaseModel):
    nodes: Optional[List] = []
    connections: List[Connection]


