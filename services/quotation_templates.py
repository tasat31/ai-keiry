from datetime import datetime
from settings import logger
from resources.keiry_db import db_read, db_write
from typing import List
from app.types.quotation_template import QuotationTemplate

def find(id=None):

    sql = """
            SELECT
                id,
                title,
                item,
                unit_price,
                quantity,
                unit,
                tax_rate,
                created_at,
                updated_at
            FROM quotation_templates
            WHERE id = '%s'
        """ % (id)

    logger.debug(sql)
    res = db_read(sql)

    data = res.fetchone()

    if data is None:
        return None

    return QuotationTemplate(
        id=data[0],
        title=data[1],
        item=data[2],
        unit_price=data[3],
        quantity=data[4],
        unit=data[5],
        tax_rate=data[6],
        created_at=data[7],
        updated_at=data[8],
    )

def list(title=None):

    if title is None:
        return []

    condition = ''
    if title is not None:
        condition = "WHERE title = '%s'" % title

    sql = """
            SELECT
                id,
                title,
                item,
                unit_price,
                quantity,
                unit,
                tax_rate,
                created_at,
                updated_at
             FROM quotation_templates
             %s
        """ % condition

    logger.debug(sql)
    res = db_read(sql)

    quotation_templates = []
    for data in res.fetchall():
        quotation_templates.append(
            QuotationTemplate(
                id=data[0],
                title=data[1],
                item=data[2],
                unit_price=data[3],
                quantity=data[4],
                unit=data[5],
                tax_rate=data[6],
                created_at=data[7],
                updated_at=data[8],
            )
        )
    
    return quotation_templates

def entry(
        quotation_template: QuotationTemplate = None
    ):

    if (quotation_template is None):
        return

    sql = """
        INSERT INTO quotation_templates(
            title,
            item,
            unit_price,
            quantity,
            unit,
            tax_rate,
            created_at,
            updated_at
        ) VALUES(
            '%s',
            '%s',
            %s,
            %s,
            '%s',
            %s,
            '%s',
            '%s'
        )
            """ % (
            quotation_template.title,
            quotation_template.item,
            quotation_template.unit_price,
            quotation_template.quantity,
            quotation_template.unit,
            quotation_template.tax_rate,
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
            FROM quotation_templates
            WHERE id='%s'
        """ % (id)

    logger.debug(sql)
    db_write(sql)

def delete_by_title(title=None):
    if (id is None):
        return

    sql = """
            DELETE
            FROM quotation_templates
            WHERE title='%s'
        """ % (title)

    logger.debug(sql)
    db_write(sql)

def bulk_entry(csv_records: List):
    try:
        for csv_rec in csv_records[1:]:
            data = csv_rec.split(',')
            if len(data) >= 7:
                print(data)
                quotation_template = QuotationTemplate(
                    title=data[1],
                    item=data[2],
                    unit_price=data[3],
                    quantity=data[4],
                    unit=data[5],
                    tax_rate=data[6],
                )

                entry(quotation_template=quotation_template)
        return {"message": "Uploaded successfully."}
    except Exception as e:
        return {"message": f"Error: {e}"}

def quotation_template_options():
    sql = """
            SELECT
                title
             FROM quotation_templates
             GROUP BY title
             ORDER BY title
        """

    logger.debug(sql)
    res = db_read(sql)

    quotation_template_options = []
    for data in res.fetchall():
        quotation_template_options.append(data[0])

    return quotation_template_options
