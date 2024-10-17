from sqlalchemy import Column, Integer, String, Date, Double
from sqlalchemy.orm import declarative_base
from models.mixins.TimestampMixin import TimestampMixin

Base = declarative_base()

class Projects(Base, TimestampMixin):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    segment = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    launched_at = Column(Date, nullable=False)
    completed_at = Column(Date, nullable=False)
    partner = Column(String, nullable=False)
    status = Column(String, nullable=False)
    estimate_sales = Column(Integer, nullable=True)
    estimate_cost = Column(Integer, nullable=True)
    estimate_profit = Column(Integer, nullable=True)
    tax_rate = Column(Double, nullable=True)

    def __repr__(self) -> str:
        return f"Project(project_id={self.id!r})"
