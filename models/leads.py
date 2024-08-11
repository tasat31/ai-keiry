from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base
from models.mixins.TimestampMixin import TimestampMixin

Base = declarative_base()

class Leads(Base, TimestampMixin):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    entity = Column(String, nullable=False)
    postal_no = Column(String, nullable=False)
    prefecture = Column(String, nullable=False)
    city = Column(String, nullable=False)
    address = Column(String, nullable=False)
    url = Column(String)
    tel = Column(String)
    segment = Column(String, nullable=False)
    cluster = Column(String)
    trade_status = Column(String, nullable=False)
    rank = Column(String, nullable=False)
    first_contacted_at = Column(Date)
    first_contacted_media = Column(String)
    last_contacted_at = Column(Date)
    description = Column(String)
    partner_name = Column(String)
    partner_role = Column(String)
    partner_tel_1 = Column(String)
    partner_tel_2 = Column(String)
    partner_mail_address = Column(String)

    def __repr__(self) -> str:
        return f"Activity(id={self.id!r})"
