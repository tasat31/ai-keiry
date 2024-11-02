from datetime import datetime
from settings import logger
from resources.keiry_db import db_read, db_write
from typing import List
from app.types.expense_budgets import ExpenseBudget

def find(id=None):

    sql = """
            SELECT
                id,
                estimated_at,
                cost_type,
                summary,
                amount_inc_tax,
                tax_rate,
                created_at,
                updated_at
            FROM expense_budgets
            WHERE id = '%s'
        """ % (id)

    logger.debug(sql)
    res = db_read(sql)

    data = res.fetchone()

    if data is None:
        return None

    return ExpenseBudget(
        id=data[0],
        estimated_at=data[1],
        cost_type=data[2],
        summary=data[3],
        amount_inc_tax=data[4],
        tax_rate=data[5],
        created_at=data[6],
        updated_at=data[7],
    )

def list(estimated_at_from=None, estimated_at_to=None):

    condition = ''
    if (estimated_at_from is not None) and (estimated_at_to is not None):
        condition = "WHERE estimated_at BETWEEN '%s' AND '%s'" % (estimated_at_from.strftime('%Y-%m-%d'), estimated_at_to.strftime('%Y-%m-%d'))

    sql = """
            SELECT
                id,
                estimated_at,
                cost_type,
                summary,
                amount_inc_tax,
                tax_rate,
                created_at,
                updated_at
            FROM expense_budgets
            %s
        """ % (condition)

    logger.debug(sql)
    res = db_read(sql)

    expense_budgets = []
    for data in res.fetchall():
        expense_budgets.append(
            ExpenseBudget(
                id=data[0],
                estimated_at=data[1],
                cost_type=data[2],
                summary=data[3],
                amount_inc_tax=data[4],
                tax_rate=data[5],
                created_at=data[6],
                updated_at=data[7],
            )
        )

    return expense_budgets

def entry(
        expense_budget: ExpenseBudget = None
    ):

    if (expense_budget is None):
        return

    sql = """
        INSERT INTO expense_budgets(
            estimated_at,
            cost_type,
            summary,
            amount_inc_tax,
            tax_rate,
            created_at,
            updated_at
        ) VALUES(
            '%s',
            '%s',
            %s,
            '%s',
            %s,
            '%s',
            '%s',
            '%s'
        )
            """ % (
            expense_budget.estimated_at.strftime('%Y-%m-%d %H:%M:%S'),
            expense_budget.cost_type,
            expense_budget.summary,
            expense_budget.amount_inc_tax,
            expense_budget.tax_rate,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )

    logger.debug(sql)
    db_write(sql)

def delete(id=None):
    if (id is None):
        return

    sql = """
            DELETE
            FROM expense_budgets
            WHERE id='%s'
        """ % (id)

    logger.debug(sql)
    db_write(sql)

def delete_by_term(estimated_at_from=None, estimated_at_to=None):
    if (estimated_at_from is None or estimated_at_to is None):
        return

    condition = ''
    if (estimated_at_from is not None) and (estimated_at_to is not None):
        condition = "WHERE estimated_at BETWEEN '%s' AND '%s'" % (estimated_at_from.strftime('%Y-%m-%d'), estimated_at_to.strftime('%Y-%m-%d'))

    sql = """
            DELETE
            FROM expense_budgets
            %s
        """ % (condition)

    logger.debug(sql)
    db_write(sql)

def bulk_entry(csv_records: List):
    try:
        for csv_rec in csv_records[1:]:
            data = csv_rec.split(',')
            if len(data) >= 7:
                expense_budget = ExpenseBudget(
                    estimated_at=data[0],
                    cost_type=data[1],
                    summary=data[2],
                    amount_inc_tax=data[3],
                    tax_rate=data[4],
                )

                entry(expense_budget=expense_budget)
        return {"message": "Uploaded successfully."}
    except Exception as e:
        return {"message": f"Error: {e}"}
