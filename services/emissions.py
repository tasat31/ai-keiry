from datetime import datetime
from settings import logger
from resources.keiry_db import db_read, db_write
from typing import List
from app.types.emission import Emission, EmissionDetail

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

def list(entried_at_from=None, entried_at_to=None):

    condition = ''
    if (entried_at_from is not None) and (entried_at_to is not None):
        condition = "WHERE entried_at BETWEEN '%s' AND '%s'" % (entried_at_from.strftime('%Y-%m-%d'), entried_at_to.strftime('%Y-%m-%d'))

    sql = """
            SELECT
                e.journal_id as journal_id,
                j.entried_at as journal_entried_at,
                j.summary as journal_summary,
                j.remark as journal_remark,
                e.activity_id as activity_id,
                a.name as activity_name,
                a.unit as activity_unit,
                a.emission_factor as emission_factor,
                a.scope_category,
                e.activity,
                e.emission,
                e.aggregation_key,
                e.created_at,
                e.updated_at
            FROM emissions e, activities a, journals j
            WHERE journal_id IN (
                SELECT
                    id
                FROM journals
                %s
            )
            AND e.journal_id = j.id
            AND e.activity_id = a.id
        """ % (condition)

    logger.debug(sql)
    res = db_read(sql)

    emission_details = []
    for data in res.fetchall():
        emission_details.append(
            EmissionDetail(
                journal_id=data[0],
                journal_entried_at=data[1],
                journal_summary=data[2],
                journal_remark=data[3],
                activity_id=data[4],
                activity_name=data[5],
                activity_unit=data[6],
                emission_factor=data[7],
                scope_category=data[8],
                activity=data[9],
                emission=data[10],
                aggregation_key=data[11],
                created_at=data[12],
                updated_at=data[13],
            )
        )

    return emission_details

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
                    journal_id=data[1],
                    activity_id=data[2],
                    activity=data[3],
                    formula=data[4],
                    emission=data[5],
                    aggregation_key=data[6],
                )

                entry(emission=emission)
        return {"message": "Uploaded successfully."}
    except Exception as e:
        return {"message": f"Error: {e}"}

def aggregate_by_scope(entried_at_from=None, entried_at_to=None):

    condition = ''
    if (entried_at_from is not None) and (entried_at_to is not None):
        condition = "WHERE entried_at BETWEEN '%s' AND '%s'" % (entried_at_from.strftime('%Y-%m-%d'), entried_at_to.strftime('%Y-%m-%d'))

    sql = """
            SELECT
                a.scope_category,
                a.name,
                a.emission_source,
                a.unit,
                SUM(e.activity),
                SUM(e.emission)
            FROM emissions e, activities a
            WHERE e.journal_id IN (
                SELECT
                    id
                FROM journals
                %s
            )
            AND e.activity_id = a.id
            GROUP BY a.scope_category, a.name, a.emission_source, a.unit
            ORDER BY a.scope_category, a.name, a.emission_source, a.unit
        """ % (condition)

    logger.debug(sql)
    res = db_read(sql)

    aggregations_by_scope = []
    for data in res.fetchall():
        aggregations_by_scope.append(
            {
                "scope_category": data[0],
                "activity_name": data[1],
                "emission_source": data[2],
                "unit": data[3],
                "total_activity": data[4],
                "total_emission": data[5],
            }
        )

    return aggregations_by_scope

def aggregate_by_scope_and_month(entried_at_from=None, entried_at_to=None):

    condition = ''
    if (entried_at_from is not None) and (entried_at_to is not None):
        condition = "WHERE entried_at BETWEEN '%s' AND '%s'" % (entried_at_from.strftime('%Y-%m-%d'), entried_at_to.strftime('%Y-%m-%d'))

    sql = """
            SELECT
                strftime('%s', entried_at),
                a.scope_category,
                a.name,
                a.emission_source,
                a.unit,
                SUM(e.activity),
                SUM(e.emission)
            FROM emissions e, activities a, journals j
            WHERE e.journal_id IN (
                SELECT
                    id
                FROM journals
                %s
            )
            AND e.journal_id = j.id
            AND e.activity_id = a.id
            GROUP BY strftime('%s', entried_at), a.scope_category, a.name, a.emission_source, a.unit
            ORDER BY strftime('%s', entried_at), a.scope_category, a.name, a.emission_source, a.unit
        """ % ('%Y-%m', condition, '%Y-%m', '%Y-%m')

    logger.debug(sql)
    res = db_read(sql)

    aggregations_by_scope = []
    for data in res.fetchall():
        aggregations_by_scope.append(
            {
                "month": data[0],
                "scope_category": data[1],
                "activity_name": data[2],
                "emission_source": data[3],
                "unit": data[4],
                "total_activity": data[5],
                "total_emission": data[6],
            }
        )

    return aggregations_by_scope
