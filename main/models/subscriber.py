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

class Subscriber(Base):
    __tablename__ = "Subscribers"
    subscriber_id = Column(Text, primary_key=True, index=True)
    user_id = Column(Text, nullable=False)
    router_id = Column(Text, nullable=False)
    data_usage = Column(Float)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    deleted_at = Column(DateTime, index=True)
    subscription_starts_at = Column(DateTime)
    subscription_ends_at = Column(DateTime)

    