from typing import List
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FixedAsset(BaseModel):
    id: Optional[int] = None
    name: str
    launched_at: datetime
    obtained_at: datetime
    obtained_type: str
    item: str
    amount: int
    structure_or_use: str
    details: str
    depreciating_years: int
    depreciation_expense_total_at_last_fiscal_year: Optional[int] = 0
    location: str
    remark: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
