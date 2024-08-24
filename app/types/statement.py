from typing import List
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Statement(BaseModel):
    id: Optional[int] = None
    fiscal_start_date: datetime
    fiscal_end_date: datetime
    fiscal_term: str
    document_name: str
    item_name: str
    item_caption: str
    item_category: str
    display_seq: int
    amount: int
    closed: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
