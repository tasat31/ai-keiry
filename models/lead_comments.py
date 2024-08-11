from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
from models.mixins.TimestampMixin import TimestampMixin

Base = declarative_base()

class LeadComments(Base, TimestampMixin):
    __tablename__ = "lead_comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(Integer, nullable=False)
    seq = Column(Integer, nullable=False)
    posted_by = Column(String, nullable=False)
    posted_at = Column(Date, nullable=False)
    comment = Column(String, nullable=False)
    attachment_path = Column(String)

    def __repr__(self) -> str:
        return f"LeadComments(id={self.id!r})"
