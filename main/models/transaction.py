from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Text,
    Float
)
from sqlalchemy.dialects.postgresql import UUID

from main.db.dbpostgres.baseclass import Base

class Transaction(Base):
    __tablename__ = "Transactions"
    transaction_id = Column(Text, primary_key=True, index=True)
    type = Column(Text, nullable=False)
    status = Column(Text)
    payment_method = Column(Text)
    amount = Column(Float)
    qr_code_string = Column(Text)
    charge_reference = Column(Text)
    retrieval_reference = Column(Text)
    retrieval_timestamp = Column(Text)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    deleted_at = Column(DateTime, index=True)

