import json
import pandas as pd
from datetime import datetime
from settings import logger
from resources.keiry_db import db_read, db_write
from typing import List
from app.types.lead_thread import LeadThread

def find(lead_id=None):

    sql = """
            SELECT
                lead_id,
                array_comments,
                array_attachments,
                created_at,
                updated_at
            FROM lead_threads
            WHERE lead_id = '%s'
        """ % (lead_id)

    logger.debug(sql)
    res = db_read(sql)

    data = res.fetchone()

    if data is None:
        return None

    return LeadThread(
        lead_id=data[0],
        array_comments=json.loads(data[1]),
        array_attachments=json.loads(data[2]),
        created_at=data[3],
        updated_at=data[4],
    )

def save(
    lead_thread: LeadThread = None
):

    if (lead_thread is None):
        return

    lead_thread_saved = find(lead_id=lead_thread.lead_id)

    if (lead_thread_saved is None):
        sql = """
            INSERT INTO lead_threads(
                lead_id,
                array_comments,
                array_attachments,
                created_at,
                updated_at
            ) VALUES(
                %s,
                '%s',
                '%s',
                '%s',
                '%s'
            )
        """ % (
            lead_thread.lead_id,
            json.dumps(lead_thread.array_comments, indent=None),
            json.dumps(lead_thread.array_attachments, indent=None),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )
    else:
        sql = """
            UPDATE lead_threads
            SET
                array_comments = '%s',
                array_attachments = '%s',
                updated_at = '%s'
            WHERE lead_id = %s
        """ % (
            json.dumps(lead_thread.array_comments),
            json.dumps(lead_thread.array_attachments),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            lead_thread.lead_id,
        )


    logger.debug(sql)
    db_write(sql)

def delete(lead_id=None):
    if (lead_id is None):
        return

    sql = """
            DELETE
            FROM lead_theads
            WHERE lead_id='%s'
        """ % (id)

    logger.debug(sql)
    db_write(sql)
