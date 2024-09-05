from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime


class Connections(BaseModel):
    ip: Optional[Dict[str, str]]

    class Config:
        from_attributes = True  # Adjust for Pydantic V2 changes


class Devices(BaseModel):
    host: str
    layer: int
    FastEthernet0_0_mac: str
    FastEthernet0_0_IP: str
    FastEthernet0_1_mac: str
    FastEthernet0_1_IP: str
    FastEthernet1_0_mac: str
    FastEthernet1_0_IP: str
    password: str
    secret: str
    snmp_username: str
    snmp_password: str
    snmp_encryption_key: str
    meta: Optional[Dict[str, str]]  # Assuming meta is a dictionary with string keys and values

    class Config:
        from_attributes = True  # Adjust for Pydantic V2 changes


class Status(BaseModel):
    host: str
    status: bool

    class Config:
        from_attributes = True  # Adjust for Pydantic V2 changes
