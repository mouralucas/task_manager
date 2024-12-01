import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, TEXT, ForeignKey
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()


class TaskStatusModel(Base):
    """
    Model for task status.
    """
    __tablename__ = 'task_status'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)


class TaskModel(Base):
    """
    Model for tasks
    """
    __tablename__ = 'task'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    date: Mapped[datetime] = mapped_column(type_=TIMESTAMP(timezone=True))
    description: Mapped[str] = mapped_column(type_=TEXT)
    status_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('task_status.id'))
    status: Mapped[TaskStatusModel] =  relationship(foreign_keys=[status_id], lazy='subquery')