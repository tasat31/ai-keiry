from typing import List
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Emission(BaseModel):
    id: Optional[int] = None
    journal_id: str
    activity_id: str
    activity: float
    formula: str
    emission: float
    aggregation_key: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
