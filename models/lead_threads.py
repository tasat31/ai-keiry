from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import declarative_base
from models.mixins.TimestampMixin import TimestampMixin

Base = declarative_base()

class LeadThreads(Base, TimestampMixin):
    __tablename__ = "lead_threads"

    lead_id = Column(Integer, primary_key=True)
    array_comments = Column(Text)
    array_attachments = Column(Text)

    def __repr__(self) -> str:
        return f"LeadThread(id={self.id!r})"
