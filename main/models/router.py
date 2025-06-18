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
    data_usage = Column(Float)
    subscribers_count = Column(Integer, default=0)
    long = Column(Float)
    lat = Column(Float)
    is_active = Column(Boolean)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    deleted_at = Column(DateTime, index=True)