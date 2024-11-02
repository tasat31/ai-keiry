from typing import List
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GeneralCostPlan(BaseModel):
    month: str
    cost_type: str
    amount_inc_tax: int

class SalesPlan(BaseModel):
    month: str
    cost_type: str
    amount_inc_tax: int
