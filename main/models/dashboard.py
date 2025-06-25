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

class Dashboard(Base):
    __tablename__ = "Dashboard"
    type = Column(Text, primary_key=True, index=True)
    total_online_subscriber = Column(Integer)
    total_online_router = Column(Integer)
    total_data_usage = Column(Float)
    last_updated_at = Column(DateTime, index=True)