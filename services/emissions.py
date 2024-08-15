from datetime import datetime
from settings import logger
from resources.keiry_db import db_read, db_write
from typing import List
from app.types.emission import Emission

def find(id=None):

    sql = """
            SELECT
                id,
                journal_id,
                activity_id,
                activity,
                formula,
                emission,
                aggregation_key,
                created_at,
                updated_at
            FROM emissions
            WHERE id = '%s'
        """ % (id)

    logger.debug(sql)
    res = db_read(sql)

    data = res.fetchone()

    if data is None:
        return None

    return Emission(
        id=data[0],
        journal_id=data[1],
        activity_id=data[2],
        activity=data[3],
        formula=data[4],
        emission=data[5],
        aggregation_key=data[6],
        created_at=data[7],
        updated_at=data[8],
    )

def list():
    sql = """
            SELECT
                id,
                journal_id,
                activity_id,
                activity,
                formula,
                emission,
                aggregation_key,
                created_at,
                updated_at
            FROM emissions
        """

    logger.debug(sql)
    res = db_read(sql)

    activities = []
    for data in res.fetchall():
        activities.append(
            Emission(
                id=data[0],
                journal_id=data[1],
                activity_id=data[2],
                activity=data[3],
                formula=data[4],
                emission=data[5],
                aggregation_key=data[6],
                created_at=data[7],
                updated_at=data[8],
            )
        )
    
    return activities

def entry(
        emission: Emission = None
    ):

    if (emission is None):
        return

    sql = """
        INSERT INTO emissions(
            journal_id,
            activity_id,
            activity,
            formula,
            emission,
            aggregation_key,
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
            emission.journal_id,
            emission.activity_id,
            emission.activity,
            emission.formula,
            emission.emission,
            emission.aggregation_key,
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
            FROM emissions
            WHERE id='%s'
        """ % (id)

    logger.debug(sql)
    db_write(sql)

def bulk_entry(csv_records: List):
    try:
        for csv_rec in csv_records[1:]:
            data = csv_rec.split(',')
            if len(data) >= 6:
                emission = Emission(
                    journal_id=data[0],
                    activity_id=data[1],
                    activity=data[2],
                    formula=data[3],
                    emission=data[4],
                    aggregation_key=data[5],
                )

                entry(emission=emission)
        return {"message": "Uploaded successfully."}
    except Exception as e:
        return {"message": f"Error: {e}"}
