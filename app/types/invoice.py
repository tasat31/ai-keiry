from typing import List
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import pandas as pd

class InvoicePaper(BaseModel):
    id: Optional[int] = None
    issued_at: datetime
    customer: str
    title: str
    delivery_date: datetime
    payment: str
    remark: str
    details: pd.DataFrame
    account_information: str
    company_name: str
    company_postal_no: str
    company_address: str
    company_tax_no: str
    company_tel: str
    company_mail: str

    class Config:
        arbitrary_types_allowed = True
