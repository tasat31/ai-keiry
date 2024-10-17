from typing import List
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Journal(BaseModel):
    id: Optional[int] = None
    entried_at: datetime
    credit: str
    debit: str
    amount: int
    tax_rate: float
    tax: int
    summary: str
    remark: Optional[str] = ''
    partner: Optional[str] = ''
    cash_in: int = 0
    cash_out: int = 0
    tax_in: int = 0
    tax_out: int = 0
    cost_type: Optional[str] = ''
    segment: Optional[str] = ''
    project_id: Optional[int] = None
    fiscal_term: str
    month: str
    closed: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
