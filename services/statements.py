from datetime import datetime
from settings import logger
from resources.keiry_db import db_read, db_write
from typing import List
from app.types.statement import Statement

def find(id=None):

    sql = """
            SELECT
                id,
                fiscal_start_date,
                fiscal_end_date,
                fiscal_term,
                document_name,
                item_name,
                item_caption,
                item_category,
                display_seq,
                amount,
                closed,
                created_at,
                updated_at
            FROM statements
            WHERE id = '%s'
        """ % (id)

    logger.debug(sql)
    res = db_read(sql)

    data = res.fetchone()

    if data is None:
        return None

    return Statement(
        id=data[0],
        fiscal_start_date=data[1],
        fiscal_end_date=data[2],
        fiscal_term=data[3],
        document_name=data[4],
        item_name=data[5],
        item_caption=data[6],
        item_category=data[7],
        display_seq=data[8],
        amount=data[9],
        closed=data[10],
        created_at=data[11],
        updated_at=data[12],
    )

def list(fiscal_term=None, document_name=None):

    if fiscal_term is None or document_name is None:
        return []

    condition = "WHERE fiscal_term = '%s' AND document_name ='%s'" % (fiscal_term, document_name)

    sql = """
            SELECT
                id,
                fiscal_start_date,
                fiscal_end_date,
                fiscal_term,
                document_name,
                item_name,
                item_caption,
                item_category,
                display_seq,
                amount,
                closed,
                created_at,
                updated_at
            FROM statements
             %s
        """ % condition

    logger.debug(sql)
    res = db_read(sql)

    statements = []
    for data in res.fetchall():
        statements.append(
            Statement(
                id=data[0],
                fiscal_start_date=data[1],
                fiscal_end_date=data[2],
                fiscal_term=data[3],
                document_name=data[4],
                item_name=data[5],
                item_caption=data[6],
                item_category=data[7],
                display_seq=data[8],
                amount=data[9],
                closed=data[10],
                created_at=data[11],
                updated_at=data[12],
            )
        )
    
    return statements

def entry(
        statement: Statement = None
    ):

    if (statement is None):
        return

    sql = """
        INSERT INTO statements(
            fiscal_start_date,
            fiscal_end_date,
            fiscal_term,
            document_name,
            item_name,
            item_caption,
            item_category,
            display_seq,
            amount,
            closed,
            created_at,
            updated_at
        ) VALUES(
            '%s',
            '%s',
            '%s',
            '%s',
            '%s',
            '%s',
            '%s',
            %s,
            %s,
            '%s',
            '%s',
            '%s'
        )
            """ % (
            statement.fiscal_start_date.strftime('%Y-%m-%d %H:%M:%S'),
            statement.fiscal_end_date.strftime('%Y-%m-%d %H:%M:%S'),
            statement.fiscal_term,
            statement.document_name,
            statement.item_name,
            statement.item_caption,
            statement.item_category,
            statement.display_seq,
            statement.amount,
            statement.closed,
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
            FROM statements
            WHERE id='%s'
        """ % (id)

    logger.debug(sql)
    db_write(sql)

def delete_by_fiscal_term(fiscal_term=None):
    if fiscal_term is None:
        return

    sql = """
            DELETE
            FROM statements
            WHERE fiscal_term = '%s'
        """ % fiscal_term

    logger.debug(sql)
    db_write(sql)

def bulk_entry(csv_records: List):
    try:
        for csv_rec in csv_records[1:]:
            data = csv_rec.split(',')
            print(data)
            if len(data) >= 9:
                statement = Statement(
                    fiscal_start_date=data[1],
                    fiscal_end_date=data[2],
                    fiscal_term=data[3],
                    document_name=data[4],
                    item_name=data[5],
                    item_caption=data[6],
                    item_category='',
                    display_seq=data[7],
                    amount=data[8],
                    closed=True,
                )

                entry(statement=statement)
        return {"message": "Uploaded successfully."}
    except Exception as e:
        return {"message": f"Error: {e}"}
