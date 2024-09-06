from typing import List
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import pandas as pd

class Quotation(BaseModel):
    id: Optional[int] = None
    issued_at: datetime
    customer: str
    title: str
    delivery: str
    expiry: str
    payment: str
    other_conditions: List
    remark: str
    departure: str
    arrival: str
    trip: str
    details: pd.DataFrame
    company_name: str
    company_postal_no: str
    company_address: str
    company_tax_no: str
    company_tel: str
    company_mail: str

    class Config:
        arbitrary_types_allowed = True
