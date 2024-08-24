from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import declarative_base
from models.mixins.TimestampMixin import TimestampMixin

Base = declarative_base()

class Statements(Base, TimestampMixin):
    __tablename__ = "statements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fiscal_start_date = Column(Date, nullable=False)
    fiscal_end_date = Column(Date, nullable=False)
    fiscal_term = Column(String, nullable=False)
    document_name = Column(String, nullable=False)
    item_name = Column(String, nullable=False)
    item_caption = Column(String, nullable=False)
    item_category = Column(String, nullable=False)
    display_seq = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    closed = Column(Boolean, nullable=False)

    def __repr__(self) -> str:
        return f"Statement(ide={self.id!r})"
