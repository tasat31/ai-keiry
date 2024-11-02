from sqlalchemy import Column, Integer, String, Date, Double, Boolean
from sqlalchemy.orm import declarative_base
from models.mixins.TimestampMixin import TimestampMixin

Base = declarative_base()

class ExpenseBudgets(Base, TimestampMixin):
    __tablename__ = "expense_budgets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    estimated_at = Column(Date, nullable=False)
    cost_type = Column(String, nullable=False)
    summary = Column(String, nullable=False)
    amount_inc_tax = Column(Integer, nullable=False)
    tax_rate = Column(Double, nullable=False)

    def __repr__(self) -> str:
        return f"ExpenseBudgets(id={self.id!r})"
