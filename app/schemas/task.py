from common.enums import TaskPriority, TaskStatus
from database import Base
from schemas.base_entity import BaseEntity
from sqlalchemy import Column, Enum, ForeignKey, String
from sqlalchemy import Uuid as SqlAlchemyUUID
from sqlalchemy.orm import relationship


class Task(BaseEntity, Base):
    __tablename__ = "tasks"

    summary = Column(String, nullable=True)
    description = Column(String, nullable=True)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.BACKLOG)
    priority = Column(Enum(TaskPriority), nullable=False, default=TaskPriority.LOW)

    owner_id = Column(SqlAlchemyUUID, ForeignKey("users.id"), nullable=True)

    owner = relationship("User", back_populates="tasks")
