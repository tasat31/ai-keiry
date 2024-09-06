from datetime import datetime, timedelta
from settings import logger
from resources.keiry_db import db_read, db_write
from typing import List

def fiscal_term_settings(fiscal_start_date=None):

    if fiscal_start_date is not None:
        update_sql = """
            UPDATE kittings
            SET
                parametar = '%s',
                updated_at = '%s'
            WHERE key = 'fiscal_start_date'
        """ % (fiscal_start_date.strftime('%Y-%m-%d'), datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        logger.debug(update_sql)
        res = db_write(update_sql)

    fetch_sql = """
        SELECT
            parametar
        FROM kittings
        WHERE key = 'fiscal_start_date'
    """

    logger.debug(fetch_sql)
    res = db_read(fetch_sql)

    data = res.fetchone()

    fiscal_start_date = datetime.strptime(data[0], '%Y-%m-%d')
    last_date = fiscal_start_date - timedelta(days=1)

    fiscal_end_date = datetime(last_date.year + 1, last_date.month, last_date.day)
 
    fiscal_term = fiscal_end_date.strftime('%Y年%m月期')

    return (fiscal_start_date, fiscal_end_date, fiscal_term)

def company_profile_settings(company_name=None, company_postal_no=None, company_address=None, company_tax_no=None, company_tel=None, company_mail=None):
    #---------------------
    #--- update kittings
    #---------------------
    # update company_name
    if company_name is not None:
        update_sql = """
            UPDATE kittings
            SET
                parametar = '%s',
                updated_at = '%s'
            WHERE key = 'company_name'
        """ % (company_name, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        logger.debug(update_sql)
        res = db_write(update_sql)

    # update company_postal_no
    if company_postal_no is not None:
        update_sql = """
            UPDATE kittings
            SET
                parametar = '%s',
                updated_at = '%s'
            WHERE key = 'company_postal_no'
        """ % (company_postal_no, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        logger.debug(update_sql)
        res = db_write(update_sql)

    # update company_address
    if company_address is not None:
        update_sql = """
            UPDATE kittings
            SET
                parametar = '%s',
                updated_at = '%s'
            WHERE key = 'company_address'
        """ % (company_address, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        logger.debug(update_sql)
        res = db_write(update_sql)

    # update company_tax_no
    if company_tax_no is not None:
        update_sql = """
            UPDATE kittings
            SET
                parametar = '%s',
                updated_at = '%s'
            WHERE key = 'company_tax_no'
        """ % (company_tax_no, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        logger.debug(update_sql)
        res = db_write(update_sql)

    # update company_tel
    if company_tel is not None:
        update_sql = """
            UPDATE kittings
            SET
                parametar = '%s',
                updated_at = '%s'
            WHERE key = 'company_tel'
        """ % (company_tel, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        logger.debug(update_sql)
        res = db_write(update_sql)

    # update company_mail
    if company_mail is not None:
        update_sql = """
            UPDATE kittings
            SET
                parametar = '%s',
                updated_at = '%s'
            WHERE key = 'company_mail'
        """ % (company_mail, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        logger.debug(update_sql)
        res = db_write(update_sql)

    #---------------------
    #--- fetch kittings
    #---------------------
    # fetch company_name
    fetch_sql = """
        SELECT
            parametar
        FROM kittings
        WHERE key = 'company_name'
    """

    logger.debug(fetch_sql)
    res = db_read(fetch_sql)

    company_name_fetched = res.fetchone()[0]

    # fetch company_postal_no
    fetch_sql = """
        SELECT
            parametar
        FROM kittings
        WHERE key = 'company_postal_no'
    """

    logger.debug(fetch_sql)
    res = db_read(fetch_sql)

    company_postal_no_fetched = res.fetchone()[0]

    # fetch company_address
    fetch_sql = """
        SELECT
            parametar
        FROM kittings
        WHERE key = 'company_address'
    """

    logger.debug(fetch_sql)
    res = db_read(fetch_sql)

    company_address_fetched = res.fetchone()[0]

    # fetch company_tax_no
    fetch_sql = """
        SELECT
            parametar
        FROM kittings
        WHERE key = 'company_tax_no'
    """

    logger.debug(fetch_sql)
    res = db_read(fetch_sql)

    company_tax_no_fetched = res.fetchone()[0]

    # fetch company_tel
    fetch_sql = """
        SELECT
            parametar
        FROM kittings
        WHERE key = 'company_tel'
    """

    logger.debug(fetch_sql)
    res = db_read(fetch_sql)

    company_tel_fetched = res.fetchone()[0]

    # fetch company_tel
    fetch_sql = """
        SELECT
            parametar
        FROM kittings
        WHERE key = 'company_mail'
    """

    logger.debug(fetch_sql)
    res = db_read(fetch_sql)

    company_mail_fetched = res.fetchone()[0]

    return (company_name_fetched, company_postal_no_fetched, company_address_fetched, company_tax_no_fetched, company_tel_fetched, company_mail_fetched)
