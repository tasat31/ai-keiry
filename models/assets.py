from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import declarative_base
from models.mixins.TimestampMixin import TimestampMixin

Base = declarative_base()

class Assets(Base, TimestampMixin):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    obtained_at = Column(Date, nullable=False)
    obtained_type = Column(String, nullable=False)
    item = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    depreciating_year = Column(Date, nullable=False)
    depreciation_expense_total = Column(Integer, nullable=False)
    closed = Column(Boolean, nullable=False)

    def __repr__(self) -> str:
        return f"Statement(ide={self.id!r})"
