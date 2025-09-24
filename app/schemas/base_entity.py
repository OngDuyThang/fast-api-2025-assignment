from uuid import uuid4

from sqlalchemy import Column, Time
from sqlalchemy import Uuid as SQLAlchemyUuid


class BaseEntity:
    id = Column(SQLAlchemyUuid, primary_key=True, default=uuid4)
    created_at = Column(Time, nullable=True)
    updated_at = Column(Time, nullable=True)
