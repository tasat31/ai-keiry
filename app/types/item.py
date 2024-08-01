from typing import List
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    caption: str
    category: str
    display_seq: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
