from datetime import datetime
from settings import logger
from resources.keiry_db import db_read
from typing import List
from app.types.business_plan import GeneralCostPlan, SalesPlan


def sales_plan_list(entried_at_from=None, entried_at_to=None):
    pass

def general_cost_plan_list(entried_at_from=None, entried_at_to=None, closed=None):
    if (entried_at_from is None) or (entried_at_to is None):
        return

    condition = ''
    if (entried_at_from is not None) and (entried_at_to is not None):
        condition = "WHERE entried_at BETWEEN '%s' AND '%s'" % (entried_at_from.strftime('%Y-%m-%d'), entried_at_to.strftime('%Y-%m-%d'))
        condition = condition + " AND credit = '販売費及び一般管理費'"
    
    if (closed is not None):
        condition = condition +" AND closed = %s" % closed

    sql = """
            SELECT
                month,
                cost_type,
                SUM(cash_out)
             FROM journals
             %s
             GROUP BY month, cost_type
             ORDER BY month, cost_type
        """ % condition

    logger.debug(sql)
    res = db_read(sql)

    general_cost_plans = []
    for data in res.fetchall():
        general_cost_plans.append(
            GeneralCostPlan(
                month=data[0],
                cost_type=data[1],
                amount_inc_tax=data[2],
            )
        )
    
    return general_cost_plans
