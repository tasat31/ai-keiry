from sqlalchemy import Column, Integer, String, Boolean, Date
from sqlalchemy.orm import declarative_base
from models.mixins.TimestampMixin import TimestampMixin
Base = declarative_base()

class FixedAssets(Base, TimestampMixin):
    __tablename__ = "fixed_assets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    launched_at = Column(Date, nullable=False)
    obtained_at = Column(Date, nullable=False)
    obtained_type = Column(String, nullable=False)
    item = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    structure_or_use = Column(String, nullable=False)  # 減価償却資産の耐用年数等に関する省令(別表第一 「構造又は用途」)
    details = Column(String, nullable=False)  # 減価償却資産の耐用年数等に関する省令(別表第一 「細目」)
    depreciating_years = Column(Integer, nullable=True)
    depreciation_expense_total_at_last_fiscal_year = Column(Integer, nullable=True)
    location = Column(String, nullable=False)
    remark = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"FixedAsset(id={self.id!r})"
