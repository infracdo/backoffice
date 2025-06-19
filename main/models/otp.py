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

class MobileOtp(Base):
    __tablename__ = "MobileOtp"
    otp_id = Column(Text, primary_key=True, index=True)
    otp = Column(Text, nullable=False)
    mobile_no = Column(Text, nullable=False)
    device_id = Column(Text)
    ref_id = Column(Text)
    created_at = Column(DateTime, index=True)