from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Text,
    Float,
    Integer
)
from sqlalchemy.dialects.postgresql import UUID

from main.db.dbpostgres.baseclass import Base

class Router(Base):
    __tablename__ = "Routers"
    router_id = Column(Text, primary_key=True, index=True)
    owner_user_id = Column(Text, nullable=False, index=True)
    serial_no = Column(Text)
    router_model = Column(Text)
    router_version = Column(Text)
    mac_address = Column(Text)
    ip_address = Column(Text)
    password = Column(Text)
    qr_string = Column(Text)
    data_usage = Column(Float, default=0)
    subscribers_count = Column(Integer, default=0)
    long = Column(Float)
    lat = Column(Float)
    created_by = Column(Text)
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    deleted_at = Column(DateTime, index=True)