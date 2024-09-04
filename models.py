from database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text


class NewConnections(Base):
    __tablename__ = 'NewConnections'
    id = Column(String, primary_key=True, nullable=False)
    src_device_id = Column(String, nullable=False)
    dst_device_id = Column(String, nullable=False)


class Devices(Base):
    __tablename__ = 'Devices'
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    layers = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    status = Column(Boolean)
    ip = Column(String, nullable=False, unique=True)
    mac = Column(String, nullable=False, unique=True)
