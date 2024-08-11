from typing import List
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TrialBalance(BaseModel):
    display_seq: int
    name: str
    caption: str
    credit_actual_total_amount: int
    debit_actual_total_amount: int
    balance_actual_amount: int
    credit_predict_total_amount: int
    debit_predict_total_amount: int
    balance_predict_amount: int
    credit_actual_predict_total_amount: int
    debit_actual_predict_total_amount: int
    balance_actual_predict_amount: int
    credit_actual_total_tax: int
    debit_actual_total_tax: int
    balance_actual_tax: int
    credit_predict_total_tax: int
    debit_predict_total_tax: int
    balance_predict_tax: int
    credit_actual_predict_total_tax: int
    debit_actual_predict_total_tax: int
    balance_actual_predict_tax: int
