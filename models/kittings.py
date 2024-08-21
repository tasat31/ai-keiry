from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from models.mixins.TimestampMixin import TimestampMixin

Base = declarative_base()

class Kittings(Base, TimestampMixin):
    __tablename__ = "kittings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String, nullable=False)
    parametar = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"Kittings(id={self.id!r})"
