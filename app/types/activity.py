from typing import List
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Activity(BaseModel):
    id: Optional[int] = None
    name: str
    emission_source: str
    unit: str
    emission_factor: float
    scope_category: str
    basis_of_emission_factor: str
    description: Optional[str] = ''
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
