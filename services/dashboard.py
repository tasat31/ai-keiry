from datetime import datetime
import pandas as pd
from settings import logger
from resources.keiry_db import db_read, db_write
from typing import List

def leads(entried_at_from=None, entried_at_to=None):

    condition = ''
    if (entried_at_from is not None) and (entried_at_to is not None):
        condition = "WHERE entried_at BETWEEN '%s' AND '%s'" % (entried_at_from.strftime('%Y-%m-%d'), entried_at_to.strftime('%Y-%m-%d'))

    sql = """
            SELECT
                count(1)
             FROM leads
             WHERE trade_status <> "削除"
             %s
        """ % condition

    logger.debug(sql)
    res = db_read(sql)

    data = res.fetchone()

    return data[0]

def sales(entried_at_from=None, entried_at_to=None):

    condition = ''
    if (entried_at_from is not None) and (entried_at_to is not None):
        condition = "WHERE entried_at BETWEEN '%s' AND '%s'" % (entried_at_from.strftime('%Y-%m-%d'), entried_at_to.strftime('%Y-%m-%d'))

    sql = """
            SELECT
                SUM(amount)
             FROM journals
             WHERE debit = '売上高' AND closed = True
             %s
        """ % condition

    logger.debug(sql)
    res = db_read(sql)

    data = res.fetchone()

    return data[0]

def expense(entried_at_from=None, entried_at_to=None):

    condition = ''
    if (entried_at_from is not None) and (entried_at_to is not None):
        condition = "WHERE entried_at BETWEEN '%s' AND '%s'" % (entried_at_from.strftime('%Y-%m-%d'), entried_at_to.strftime('%Y-%m-%d'))

    sql = """
            SELECT
                SUM(amount)
             FROM journals
             WHERE credit in ('販売費及び一般管理費', '売上原価') AND closed = True
             %s
        """ % condition

    logger.debug(sql)
    res = db_read(sql)

    data = res.fetchone()

    return data[0]

def sales_expense_leads_by_segment(entried_at_from=None, entried_at_to=None):

    condition = ''
    if (entried_at_from is not None) and (entried_at_to is not None):
        condition = "WHERE entried_at BETWEEN '%s' AND '%s'" % (entried_at_from.strftime('%Y-%m-%d'), entried_at_to.strftime('%Y-%m-%d'))

    sql = """
            WITH leads_by_segment AS (
                SELECT
                    segment,
                    COUNT(1) as cnt
                FROM leads
                WHERE trade_status <> "削除"
                group by segment            
            ),
            sales_by_segment AS (
                SELECT
                    segment,
                    SUM(amount) as amount
                 FROM journals
                WHERE debit = '売上高' AND closed = True
                %s
                group by segment
            ),
            expense_by_segment AS (
                SELECT
                    segment,
                    SUM(amount) as amount
                FROM journals
                WHERE debit = '売上原価' AND closed = True
                %s
                group by segment
            )

            SELECT
                lbs.segment,
                lbs.cnt,
                ifnull(sbs.amount, 0),
                ifnull(ebs.amount, 0),
                ifnull(sbs.amount, 0) - ifnull(ebs.amount, 0)
            FROM leads_by_segment lbs
            LEFT OUTER JOIN sales_by_segment sbs ON lbs.segment = sbs.segment
            LEFT OUTER JOIN expense_by_segment ebs ON lbs.segment = ebs.segment
        """ % (condition, condition)

    logger.debug(sql)
    res = db_read(sql)

    segment_data = []
    for data in res.fetchall():
        segment_data.append({
            "セグメント": data[0],
            "見込み客数": data[1],
            "売上高(税込)": data[2],
            "売上原価(税込)": data[3],
            "売上利益(税込)": data[4],
        })

    return pd.DataFrame(segment_data)
