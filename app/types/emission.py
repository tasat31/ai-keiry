from typing import List
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Emission(BaseModel):
    journal_id: str
    activity_id: str
    activity: float
    formula: str
    emission: float
    aggregation_key: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class EmissionDetail(BaseModel):
    journal_id: int
    journal_entried_at: datetime
    journal_summary: str
    journal_remark: str
    activity_id: int
    activity_name: str
    activity_unit: str
    emission_factor: float
    scope_category: str
    activity: float
    emission: float
    aggregation_key: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
