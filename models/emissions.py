from sqlalchemy import Column, Integer, String, Double
from sqlalchemy.orm import declarative_base
from models.mixins.TimestampMixin import TimestampMixin

Base = declarative_base()

class Emissions(Base, TimestampMixin):
    __tablename__ = "emissions"

    journal_id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, nullable=False)
    activity = Column(Double, nullable=False)
    formula = Column(String, nullable=False)
    emission = Column(Double, nullable=False)
    aggregation_key = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"Emission(id={self.id!r})"
