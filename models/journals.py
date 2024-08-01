from sqlalchemy import Column, Integer, String, Date, Double, Boolean
from sqlalchemy.orm import declarative_base
from models.mixins.TimestampMixin import TimestampMixin

Base = declarative_base()

class Journals(Base, TimestampMixin):
    __tablename__ = "journals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    entried_at = Column(Date, nullable=False)
    credit = Column(String, nullable=False)
    debit = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    tax_rate = Column(Double, nullable=False)
    tax = Column(Integer, nullable=False)
    summary = Column(String, nullable=False)
    remark = Column(String, nullable=False)
    partner = Column(String, nullable=False)
    cash_in = Column(Integer, nullable=False)
    cash_out = Column(Integer, nullable=False)
    tax_in = Column(Integer, nullable=False)
    tax_out = Column(Integer, nullable=False)
    cost_type = Column(String, nullable=False)
    segment = Column(String, nullable=False)
    project_code = Column(String, nullable=False)
    fiscal_term = Column(String, nullable=False)
    month = Column(String, nullable=False)
    closed = Column(Boolean, nullable=False)

    def __repr__(self) -> str:
        return f"Journal(id={self.id!r})"
