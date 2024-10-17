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
    actual_sales: Optional[int] = 0
    actual_cost: Optional[int] = 0
    actual_profit: Optional[int] = 0
    diff_sales: Optional[int] = 0
    diff_cost: Optional[int] = 0
    diff_profit: Optional[int] = 0
    tax_rate: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
