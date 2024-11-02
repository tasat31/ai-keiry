from typing import List
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ExpenseBudget(BaseModel):
    id: Optional[int] = None
    estimated_at: datetime
    cost_type: str
    summary: str
    amount_inc_tax: int
    tax_rate: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
