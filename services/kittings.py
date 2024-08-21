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
 
    fiscal_term = "%d年%d月期" % (fiscal_end_date.year, fiscal_end_date.month)

    return (fiscal_start_date, fiscal_end_date, fiscal_term)
