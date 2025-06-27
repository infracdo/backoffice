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

class UserRole(Base):
    __tablename__ = "UserRoles"
    type = Column(Text, primary_key=True, index=True)
    description = Column(Text)

class Tier(Base):
    __tablename__ = "Tiers"
    tier_id = Column(Text, primary_key=True, index=True)
    name = Column(Text)
    description = Column(Text)
    data_limit = Column(Float)
    is_default_tier = Column(Boolean)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    deleted_at = Column(DateTime, index=True)

class User(Base):
    __tablename__ = "Users"
    user_id = Column(Text, primary_key=True, index=True)
    user_type = Column(Text, nullable=False, index=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    mobile_no = Column(Text, nullable=False, unique=True)
    device_id = Column(Text)
    data_limit = Column(Float, default=0)
    data_usage = Column(Float, default=0)
    data_left = Column(Float, default=0)
    tier = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    last_login = Column(DateTime, index=True)
    deleted_at = Column(DateTime, index=True)

    