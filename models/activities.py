from sqlalchemy import Column, Integer, String, Double
from sqlalchemy.orm import declarative_base
from models.mixins.TimestampMixin import TimestampMixin

Base = declarative_base()

class Activities(Base, TimestampMixin):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    emission_source = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    emission_factor = Column(Double, nullable=False)
    scope_category = Column(String, nullable=False)
    basis_of_emission_factor = Column(String, nullable=False)
    description = Column(String, nullable=True)

    def __repr__(self) -> str:
        return f"Activity(id={self.id!r})"
