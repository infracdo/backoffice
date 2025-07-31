from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Text
)
from sqlalchemy.dialects.postgresql import UUID

from main.db.dbpostgres.baseclass import Base

class Promo(Base):
    __tablename__ = "Promos"
    promo_id = Column(Text, primary_key=True, index=True)
    image_url = Column(Text, nullable=False)
    link_url = Column(Text, nullable=False)
    type = Column(Text, nullable=False)
    title = Column(Text)
    description = Column(Text)
    is_show = Column(Boolean, default=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    deleted_at = Column(DateTime, index=True)

