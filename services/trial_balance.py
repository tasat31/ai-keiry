from datetime import datetime, timedelta
from settings import logger
from resources.keiry_db import db_read
from typing import List
from app.types.trial_balance import TrialBalance

def output(entried_at_from: datetime, entried_at_to: datetime):

    entried_at_from_str = entried_at_from.strftime('%Y-%m-%d')
    entried_at_to_str = entried_at_to.strftime('%Y-%m-%d')

    sql = """
        -- 借方(実績)合計
        WITH credit_actual AS (
            SELECT
                credit AS name,
                SUM(amount) AS total_amount,
                SUM(tax) AS total_tax
            FROM journals
            WHERE entried_at BETWEEN '%s' AND '%s'
              AND closed = True
            GROUP BY credit
        ),
        -- 貸方(実績)合計
        debit_actual AS (
            SELECT
                debit AS name,
                SUM(amount) AS total_amount,
                SUM(tax) AS total_tax
            FROM journals
            WHERE entried_at BETWEEN '%s' AND '%s'
                AND closed = True
            GROUP BY debit
        ),
        -- 借方(予測)合計
        credit_predict AS (
            SELECT
                credit AS name,
                SUM(amount) AS total_amount,
                SUM(tax) AS total_tax
            FROM journals
            WHERE entried_at BETWEEN '%s' AND '%s'
              AND closed = False
            GROUP BY credit
        ),
        -- 貸方(予測)合計
        debit_predict AS (
            SELECT
                debit AS name,
                SUM(amount) AS total_amount,
                SUM(tax) AS total_tax
            FROM journals
            WHERE entried_at BETWEEN '%s' AND '%s'
              AND closed = False
            GROUP BY debit
        ),
        -- 前期残高
        balance_of_last_fiscal_year AS (
            SELECT
                item_name AS name,
                amount AS total_amount
            FROM statements
            WHERE fiscal_term = '%s'
              AND closed = 'True'
        )

        SELECT
            it.display_seq AS display_seq,
            it.name AS name,
            it.caption AS caption,
            ifnull(bl.total_amount, 0) AS balance_total_amount,
            ifnull(ca.total_amount, 0) AS credit_actual_total_amount,
            ifnull(da.total_amount, 0) AS debit_actual_total_amount,
            CASE it.category
                WHEN 'PR' THEN ifnull(bl.total_amount, 0) + ifnull(da.total_amount,0) - ifnull(ca.total_amount, 0)
                WHEN 'LS' THEN ifnull(bl.total_amount, 0) + ifnull(da.total_amount,0) - ifnull(ca.total_amount, 0)
                WHEN 'CL' THEN ifnull(bl.total_amount, 0) + ifnull(da.total_amount,0) - ifnull(ca.total_amount, 0)
                WHEN 'FL' THEN ifnull(bl.total_amount, 0) + ifnull(da.total_amount,0) - ifnull(ca.total_amount, 0)
                ELSE ifnull(bl.total_amount, 0) + ifnull(ca.total_amount, 0) - ifnull(da.total_amount,0)
            END AS balance_actual_amount,
            ifnull(cp.total_amount, 0) AS credit_predict_total_amount,
            ifnull(dp.total_amount, 0) AS debit_predict_total_amount,
            CASE it.category
                WHEN 'PR' THEN ifnull(dp.total_amount, 0) - ifnull(cp.total_amount, 0)
                WHEN 'LS' THEN ifnull(dp.total_amount, 0) - ifnull(cp.total_amount, 0)
                WHEN 'CL' THEN ifnull(dp.total_amount, 0) - ifnull(cp.total_amount, 0)
                WHEN 'FL' THEN ifnull(dp.total_amount, 0) - ifnull(cp.total_amount, 0)
                ELSE ifnull(cp.total_amount, 0) - ifnull(dp.total_amount, 0)
            END AS balance_predict_amount,
            ifnull(ca.total_amount, 0) + ifnull(cp.total_amount, 0) AS credit_actual_predict_total_amount,
            ifnull(da.total_amount, 0) + ifnull(dp.total_amount, 0) AS debit_actual_predict_total_amount,
            CASE it.category
                WHEN 'PR' THEN ifnull(bl.total_amount, 0) + (ifnull(da.total_amount, 0) + ifnull(dp.total_amount,0)) - (ifnull(ca.total_amount, 0) + ifnull(cp.total_amount, 0))
                WHEN 'LS' THEN ifnull(bl.total_amount, 0) + (ifnull(da.total_amount, 0) + ifnull(dp.total_amount,0)) - (ifnull(ca.total_amount, 0) + ifnull(cp.total_amount, 0))
                WHEN 'CL' THEN ifnull(bl.total_amount, 0) + (ifnull(da.total_amount, 0) + ifnull(dp.total_amount,0)) - (ifnull(ca.total_amount, 0) + ifnull(cp.total_amount, 0))
                WHEN 'FL' THEN ifnull(bl.total_amount, 0) + (ifnull(da.total_amount, 0) + ifnull(dp.total_amount,0)) - (ifnull(ca.total_amount, 0) + ifnull(cp.total_amount, 0))
                ELSE ifnull(bl.total_amount, 0) + (ifnull(ca.total_amount, 0) + ifnull(cp.total_amount, 0)) - (ifnull(da.total_amount, 0) + ifnull(dp.total_amount,0))
            END AS balance_actual_predict_amount,
            ifnull(ca.total_tax, 0) AS credit_actual_total_tax,
            ifnull(da.total_tax, 0) AS debit_actual_total_tax,
            ifnull(ca.total_tax, 0) - ifnull(da.total_tax, 0) AS balance_actual_tax,
            ifnull(cp.total_tax, 0) AS credit_predict_total_tax,
            ifnull(dp.total_tax, 0) AS debit_predict_total_tax,
            ifnull(cp.total_tax, 0) - ifnull(dp.total_tax, 0) AS balance_predict_tax,
            ifnull(ca.total_tax, 0) + ifnull(cp.total_tax, 0) AS credit_actual_predict_total_tax,
            ifnull(da.total_tax, 0) + ifnull(dp.total_tax, 0) AS debit_actual_predict_total_tax,
            (ifnull(ca.total_tax, 0) + ifnull(cp.total_tax, 0)) - (ifnull(da.total_tax, 0) + ifnull(dp.total_tax, 0)) AS balance_actual_predict_tax
        FROM items it
        LEFT OUTER JOIN credit_actual ca ON it.name = ca.name
        LEFT OUTER JOIN debit_actual da ON it.name = da.name
        LEFT OUTER JOIN credit_predict cp ON it.name = cp.name
        LEFT OUTER JOIN debit_predict dp ON it.name = dp.name
        LEFT OUTER JOIN balance_of_last_fiscal_year bl ON it.name = bl.name
        """ % (
                entried_at_from_str, entried_at_to_str,
                entried_at_from_str, entried_at_to_str,
                entried_at_from_str, entried_at_to_str,
                entried_at_from_str, entried_at_to_str,
                (entried_at_from - timedelta(days=1)).strftime('%Y年%m月期'),
            )

    logger.debug(sql)
    res = db_read(sql)


    trial_balance_sheet = []
    for data in res.fetchall():
        trial_balance_sheet.append(
            TrialBalance(
                display_seq=data[0],
                name=data[1],
                caption=data[2],
                balance_actual_last_fiscal_year=data[3],
                credit_actual_total_amount=data[4],
                debit_actual_total_amount=data[5],
                balance_actual_amount=data[6],
                credit_predict_total_amount=data[7],
                debit_predict_total_amount=data[8],
                balance_predict_amount=data[9],
                credit_actual_predict_total_amount=data[10],
                debit_actual_predict_total_amount=data[11],
                balance_actual_predict_amount=data[12],
                credit_actual_total_tax=data[13],
                debit_actual_total_tax=data[14],
                balance_actual_tax=data[15],
                credit_predict_total_tax=data[16],
                debit_predict_total_tax=data[17],
                balance_predict_tax=data[18],
                credit_actual_predict_total_tax=data[19],
                debit_actual_predict_total_tax=data[20],
                balance_actual_predict_tax=data[21]
            )
        )
    
    return trial_balance_sheet
