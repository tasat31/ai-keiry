from typing import List
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LeadThread(BaseModel):
    lead_id: int
    array_comments: List
    array_attachments: Optional[List] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
