from datetime import datetime
from settings import logger
from resources.keiry_db import db_read, db_write
from typing import List
from app.types.journal import Journal

def find(id=None):

    sql = """
            SELECT
                id,
                entried_at,
                credit,
                debit,
                amount,
                tax_rate,
                tax,
                summary,
                remark,
                partner,
                cash_in,
                cash_out,
                tax_in,
                tax_out,
                cost_type,
                segment,
                project_code,
                fiscal_term,
                month,
                closed,
                created_at,
                updated_at
            FROM journals
            WHERE id = '%s'
        """ % (id)

    logger.debug(sql)
    res = db_read(sql)

    data = res.fetchone()

    if data is None:
        return None

    return Journal(
        id=data[0],
        entried_at=data[1],
        credit=data[2],
        debit=data[3],
        amount=data[4],
        tax_rate=data[5],
        tax=data[6],
        summary=data[7],
        remark=data[8],
        partner=data[9],
        cash_in=data[10],
        cash_out=data[11],
        tax_in=data[12],
        taxt_out=data[13],
        cost_type=data[14],
        segment=data[15],
        project_code=data[16],
        fiscal_term=data[17],
        month=data[18],
        closed=data[19],
        created_at=data[20],
        updated_at=data[21],
    )

def list(entried_at_from=None, entried_at_to=None, credit_selected='ALL', debit_selected='ALL', summary_input='', partner_input=''):

    condition = ''
    if (entried_at_from is not None) and (entried_at_to is not None):
        condition = "WHERE entried_at BETWEEN '%s' AND '%s'" % (entried_at_from.strftime('%Y-%m-%d'), entried_at_to.strftime('%Y-%m-%d'))
        if (credit_selected != 'ALL'):
            condition = condition + " AND credit = '%s'" % credit_selected
        
        if (debit_selected != 'ALL'):
            condition = condition + " AND debit = '%s'" % debit_selected

        if (summary_input != ''):
            condition = condition + " AND summary LIKE '%" + summary_input + "%'"

        if (partner_input != ''):
            condition = condition + " AND partner LIKE '%" + partner_input + "%'"

    sql = """
            SELECT
                id,
                entried_at,
                credit,
                debit,
                amount,
                tax_rate,
                tax,
                summary,
                remark,
                partner,
                cash_in,
                cash_out,
                tax_in,
                tax_out,
                cost_type,
                segment,
                project_code,
                fiscal_term,
                month,
                closed,
                created_at,
                updated_at
             FROM journals
             %s 
             ORDER BY entried_at, credit, cost_type
        """ % condition

    logger.debug(sql)
    res = db_read(sql)

    journals = []
    for data in res.fetchall():
        journals.append(
            Journal(
                id=data[0],
                entried_at=data[1],
                credit=data[2],
                debit=data[3],
                amount=data[4],
                tax_rate=data[5],
                tax=data[6],
                summary=data[7],
                remark=data[8],
                partner=data[9],
                cash_in=data[10],
                cash_out=data[11],
                tax_in=data[12],
                tax_out=data[13],
                cost_type=data[14],
                segment=data[15],
                project_code=data[16],
                fiscal_term=data[17],
                month=data[18],
                closed=data[19],
                created_at=data[20],
                updated_at=data[21],
            )
        )
    
    return journals

def entry(
        journal: Journal = None
    ):

    if (journal is None):
        return

    sql = """
        INSERT INTO journals(
            entried_at,
            credit,
            debit,
            amount,
            tax_rate,
            tax,
            summary,
            remark,
            partner,
            cash_in,
            cash_out,
            tax_in,
            tax_out,
            cost_type,
            segment,
            project_code,
            fiscal_term,
            month,
            closed,
            created_at,
            updated_at
        ) VALUES(
            '%s',
            '%s',
            '%s',
            %s,
            %s,
            %s,
            '%s',
            '%s',
            '%s',
            %s,
            %s,
            %s,
            %s,
            '%s',
            '%s',
            '%s',
            '%s',
            '%s',
            %s,
            '%s',
            '%s'
        )
            """ % (
            journal.entried_at.strftime('%Y-%m-%d'),
            journal.credit,
            journal.debit,
            journal.amount,
            journal.tax_rate,
            journal.tax,
            journal.summary,
            journal.remark,
            journal.partner,
            journal.cash_in,
            journal.cash_out,
            journal.tax_in,
            journal.tax_out,
            journal.cost_type,
            journal.segment,
            journal.project_code,
            journal.fiscal_term,
            journal.month,
            journal.closed,
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
            FROM journals
            WHERE id='%s'
        """ % (id)

    logger.debug(sql)
    db_write(sql)

def bulk_entry(csv_records: List):
    try:
        for csv_rec in csv_records:
            data = csv_rec.split(',')
            if len(data) >= 16:
                journal = Journal(
                    entried_at=data[0],
                    credit=data[1],
                    debit=data[2],
                    amount=data[3],
                    tax_rate=data[4],
                    tax=data[5],
                    summary=data[6],
                    remark=data[7],
                    partner=data[8],
                    cash_in=data[9],
                    cash_out=data[10],
                    cost_type=data[11],
                    project_code=data[12],
                    fiscal_term=data[13],
                    month=data[14],
                    closed=data[15],
                )

                entry(journal=journal)
        return {"message": "Uploaded successfully."}
    except Exception as e:
        return {"message": f"Error: {e}"}

def list_by_promotion(entried_at_from=None, entried_at_to=None):

    condition = ''
    if (entried_at_from is not None) and (entried_at_to is not None):
        condition = "WHERE entried_at BETWEEN '%s' AND '%s'" % (entried_at_from.strftime('%Y-%m-%d'), entried_at_to.strftime('%Y-%m-%d'))
        condition = condition + " AND credit = '販売費及び一般管理費'"
        condition = condition + " AND cost_type IN ('荷造費', '運搬費', '広告宣伝費', '見本費', '外注費', '旅費交通費', '通勤費', '通信費', '水道光熱費', '事務用消耗品費', '消耗工具器具備品費', '修繕費', '賃借料')"
        condition = condition + " AND closed = True"

    sql = """
            SELECT
                id,
                entried_at,
                credit,
                debit,
                amount,
                tax_rate,
                tax,
                summary,
                remark,
                partner,
                cash_in,
                cash_out,
                tax_in,
                tax_out,
                cost_type,
                segment,
                project_code,
                fiscal_term,
                month,
                closed,
                created_at,
                updated_at
             FROM journals
             %s
             ORDER BY entried_at, credit, cost_type
        """ % condition

    logger.debug(sql)
    res = db_read(sql)

    journals = []
    for data in res.fetchall():
        journals.append(
            Journal(
                id=data[0],
                entried_at=data[1],
                credit=data[2],
                debit=data[3],
                amount=data[4],
                tax_rate=data[5],
                tax=data[6],
                summary=data[7],
                remark=data[8],
                partner=data[9],
                cash_in=data[10],
                cash_out=data[11],
                tax_in=data[12],
                tax_out=data[13],
                cost_type=data[14],
                segment=data[15],
                project_code=data[16],
                fiscal_term=data[17],
                month=data[18],
                closed=data[19],
                created_at=data[20],
                updated_at=data[21],
            )
        )

    return journals
