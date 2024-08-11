from datetime import datetime
from settings import logger
from resources.keiry_db import db_read, db_write
from typing import List
from app.types.activity import Activity

def find(id=None):

    sql = """
            SELECT
                id,
                name,
                emission_source,
                unit,
                emission_factor,
                scope_category,
                basis_of_emission_factor,
                description,
                created_at,
                updated_at
            FROM activities
            WHERE id = '%s'
        """ % (id)

    logger.debug(sql)
    res = db_read(sql)

    data = res.fetchone()

    if data is None:
        return None

    return Activity(
        id=data[0],
        name=data[1],
        emission_source=data[2],
        unit=data[3],
        emission_factor=data[4],
        scope_category=data[5],
        basis_of_emission_factor=data[6],
        description=data[7],
        created_at=data[8],
        updated_at=data[9],
    )

def list():
    sql = """
            SELECT
                id,
                name,
                emission_source,
                unit,
                emission_factor,
                scope_category,
                basis_of_emission_factor,
                description,
                created_at,
                updated_at
             FROM activities
        """

    logger.debug(sql)
    res = db_read(sql)

    activities = []
    for data in res.fetchall():
        activities.append(
            Activity(
                id=data[0],
                name=data[1],
                emission_source=data[2],
                unit=data[3],
                emission_factor=data[4],
                scope_category=data[5],
                basis_of_emission_factor=data[6],
                description=data[7],
                created_at=data[8],
                updated_at=data[9],
            )
        )
    
    return activities

def entry(
        activity: Activity = None
    ):

    if (activity is None):
        return

    sql = """
        INSERT INTO leads(
            name,
            emission_source,
            unit,
            emission_factor,
            scope_category,
            basis_of_emission_factor,
            description,
            created_at,
            updated_at
        ) VALUES(
            '%s',
            '%s',
            '%s',
            %s,
            '%s',
            '%s',
            '%s',
            '%s'
        )
            """ % (
            activity.name,
            activity.emission_source,
            activity.unit,
            activity.emission_factor,
            activity.scope_category,
            activity.basis_of_emission_factor,
            activity.description,
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
            FROM activities
            WHERE id='%s'
        """ % (id)

    logger.debug(sql)
    db_write(sql)

def bulk_entry(csv_records: List):
    try:
        for csv_rec in csv_records:
            data = csv_rec.split(',')
            if len(data) >= 7:
                activity = Activity(
                    name=data[0],
                    emission_source=data[1],
                    unit=data[2],
                    emission_factor=data[3],
                    scope_category=data[4],
                    basis_of_emission_factor=data[5],
                    description=data[6],
                )

                entry(activity=activity)
        return {"message": "Uploaded successfully."}
    except Exception as e:
        return {"message": f"Error: {e}"}
