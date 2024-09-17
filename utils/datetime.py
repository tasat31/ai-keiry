import datetime
from dateutil.relativedelta import relativedelta

def list_by_month(start_date=None, end_date=None)->list:
    months_list = []
    if (start_date is None or end_date is None):
        return months_list
    
    current_date = start_date
    while current_date <= end_date:
        months_list.append(current_date)
        # Move to the next month
        current_date += relativedelta(months=1)
    
    return months_list
