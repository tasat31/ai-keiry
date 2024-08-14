from typing import List
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Project(BaseModel):
    id: Optional[int] = None
    segment: str
    title: str
    description: Optional[str] = ''
    launched_at: datetime
    completed_at: datetime
    partner: str
    status: str
    estimate_sales: int
    estimate_cost: int
    estimate_profit: int
    tax_rate: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
