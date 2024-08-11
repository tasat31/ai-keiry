from sqlalchemy import Column, Integer, String, Double
from sqlalchemy.orm import declarative_base
from models.mixins.TimestampMixin import TimestampMixin

Base = declarative_base()

class Emissions(Base, TimestampMixin):
    __tablename__ = "emissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    journal_id = Column(Integer, nullable=False)
    activity_id = Column(Integer, nullable=False)
    emission_factor = Column(Double, nullable=False)
    formula = Column(String, nullable=False)
    emissions = Column(Double, nullable=False)

    def __repr__(self) -> str:
        return f"Emission(id={self.id!r})"
