from typing import List
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class QuotationTemplate(BaseModel):
    id: Optional[int] = None
    title: str
    item: str
    unit_price: int
    quantity: int
    unit: str
    tax_rate: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
