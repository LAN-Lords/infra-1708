from database import Base
from sqlalchemy import Column, Integer, String, Boolean, JSON, func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class Connections(Base):
    __tablename__ = 'connections'

    id = Column(Integer, primary_key=True)
    ip = Column(JSON, nullable=False, default=[])  # Assuming this stores a set of IP addresses
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class Devices(Base):
    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    host = Column(String(255))
    layer = Column(Integer)
    FastEthernet0_0_mac = Column(String(255))
    FastEthernet0_0_IP = Column(String(255))
    FastEthernet0_1_mac = Column(String(255))
    FastEthernet0_1_IP = Column(String(255))
    FastEthernet1_0_mac = Column(String(255))
    FastEthernet1_0_IP = Column(String(255))
    password = Column(String(255))
    secret = Column(String(255))
    snmp_username = Column(String(255))
    snmp_password = Column(String(255))
    snmp_encryption_key = Column(String(255))
    meta = Column(JSON)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class Status(Base):
    __tablename__ = 'status'

    id = Column(Integer, primary_key=True)
    host = Column(String(255))
    status = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())