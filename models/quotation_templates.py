from sqlalchemy import Column, Integer, String, Double
from sqlalchemy.orm import declarative_base
from models.mixins.TimestampMixin import TimestampMixin

Base = declarative_base()

class QuotationTemplates(Base, TimestampMixin):
    __tablename__ = "quotation_templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    item = Column(String, nullable=False)
    unit_price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit = Column(String, nullable=False)
    tax_rate = Column(Double, nullable=False)

    def __repr__(self) -> str:
        return f"QuotationTemplates(id={self.id!r})"
