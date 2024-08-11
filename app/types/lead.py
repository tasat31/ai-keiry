from typing import List
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Lead(BaseModel):
    id: Optional[int] = None
    name: str
    entity: str
    postal_no: str
    prefecture: str
    city: str 
    address: str 
    url: Optional[str] = ''
    tel: Optional[str] = ''
    segment: str 
    cluster: Optional[str] = ''
    trade_status: str 
    rank: str 
    first_contacted_at: Optional[datetime] = None
    first_contacted_media: Optional[str] = ''
    last_contacted_at: Optional[datetime] = None
    description: Optional[str] = ''
    partner_name: Optional[str] = ''
    partner_role: Optional[str] = ''
    partner_tel_1: Optional[str] = ''
    partner_tel_2: Optional[str] = ''
    partner_mail_address: Optional[str] = ''
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
