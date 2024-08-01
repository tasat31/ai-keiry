from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from models.mixins.TimestampMixin import TimestampMixin

Base = declarative_base()

class Items(Base, TimestampMixin):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    caption = Column(String, nullable=False)
    category = Column(String, nullable=False)
    display_seq = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        return f"Item(id={self.id!r})"
