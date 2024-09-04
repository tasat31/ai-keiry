import pandas as pd
from datetime import datetime
from settings import logger
from resources.keiry_db import db_read, db_write
from typing import List
from app.types.project import Project

def find(id=None):

    sql = """
            SELECT
                id,
                segment,
                title,
                description,
                launched_at,
                completed_at,
                partner,
                status,
                estimate_sales,
                estimate_cost,
                estimate_profit,
                tax_rate,
                created_at,
                updated_at
            FROM projects
            WHERE id = '%s'
        """ % (id)

    logger.debug(sql)
    res = db_read(sql)

    data = res.fetchone()

    if data is None:
        return None

    return Project(
        id=data[0],
        segment=data[1],
        title=data[2],
        description=data[3],
        launched_at=data[4],
        completed_at=data[5],
        partner=data[6],
        status=data[7],
        estimate_sales=data[8],
        estimate_cost=data[9],
        estimate_profit=data[10],
        created_at=data[11],
        updated_at=data[12],
    )

def list():
    sql = """
            SELECT
                id,
                segment,
                title,
                description,
                launched_at,
                completed_at,
                partner,
                status,
                estimate_sales,
                estimate_cost,
                estimate_profit,
                tax_rate,
                created_at,
                updated_at
             FROM projects
             ORDER BY segment, launched_at
        """

    logger.debug(sql)
    res = db_read(sql)

    projects = []
    for data in res.fetchall():
        projects.append(
            Project(
                id=data[0],
                segment=data[1],
                title=data[2],
                description=data[3],
                launched_at=data[4],
                completed_at=data[5],
                partner=data[6],
                status=data[7],
                estimate_sales=data[8],
                estimate_cost=data[9],
                estimate_profit=data[10],
                tax_rate=data[11],
                created_at=data[12],
                updated_at=data[13],
            )
        )
    
    return projects

def entry(
        project: Project = None
    ):

    if (project is None):
        return

    sql = """
        INSERT INTO projects(
            segment,
            title,
            description,
            launched_at,
            completed_at,
            partner,
            status,
            estimate_sales,
            estimate_cost,
            estimate_profit,
            tax_rate,
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
            %s,
            %s,
            '%s',
            '%s'
        )
            """ % (
            project.segment,
            project.title,
            project.description,
            project.launched_at.strftime('%Y-%m-%d'),
            project.completed_at.strftime('%Y-%m-%d'),
            project.partner,
            project.status,
            project.estimate_sales,
            project.estimate_cost,
            project.estimate_profit,
            project.tax_rate,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )

    logger.debug(sql)
    db_write(sql)

def update(
        project: Project = None
    ):

    if (project is None):
        return

    sql = """
        UPDATE projects
            SET
                segment = '%s',
                title = '%s',
                description = '%s',
                launched_at = '%s',
                completed_at = '%s',
                partner = '%s',
                status = '%s',
                estimate_sales = '%s',
                estimate_cost = '%s',
                estimate_profit = '%s',
                tax_rate = '%s',
                updated_at = '%s'
        WHERE id = %s
    """ % (
            project.segment,
            project.title,
            project.description,
            project.launched_at.strftime('%Y-%m-%d'),
            project.completed_at.strftime('%Y-%m-%d'),
            project.partner,
            project.status,
            project.estimate_sales,
            project.estimate_cost,
            project.estimate_profit,
            project.tax_rate,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            project.id,
        )

    logger.debug(sql)
    db_write(sql)

def delete(id=None):
    if (id is None):
        return

    sql = """
            DELETE
            FROM projects
            WHERE id='%s'
        """ % (id)

    logger.debug(sql)
    db_write(sql)

def bulk_entry(csv_records: List):
    try:
        for csv_rec in csv_records:
            data = csv_rec.split(',')
            if len(data) >= 13:
                project = Project(
                    id=data[0],
                    segment=data[1],
                    title=data[2],
                    description=data[3],
                    launched_at=data[4],
                    completed_at=data[5],
                    partner=data[6],
                    status=data[7],
                    estimate_sales=data[8],
                    estimate_cost=data[9],
                    estimate_profit=data[10],
                    tax_rate=data[11],
                    created_at=data[12],
                    updated_at=data[13],
                )

                entry(project=project)
        return {"message": "Uploaded successfully."}
    except Exception as e:
        return {"message": f"Error: {e}"}

def bulk_update(df: pd.DataFrame):
    try:
        csv_records = df.to_csv().split('\n')
        for csv_rec in csv_records[1:]:
            data = csv_rec.split(',')
            if len(data) >= 12:
                project = Project(
                    segment=data[2],
                    title=data[3],
                    description=data[4],
                    launched_at=data[5],
                    completed_at=data[6],
                    partner=data[7],
                    status=data[8],
                    estimate_sales=data[9],
                    estimate_cost=data[10],
                    estimate_profit=data[11],
                    tax_rate=data[12],
                    id=data[13],
                )

                update(project=project)
        return {"message": "Uploaded successfully."}
    except Exception as e:
        return {"message": f"Error: {e}"}

def project_options():
    sql = """
            SELECT
                title,
                updated_at
             FROM projects
             GROUP BY title, updated_at
             ORDER BY updated_at
        """

    logger.debug(sql)
    res = db_read(sql)

    project_options = []
    for data in res.fetchall():
        project_options.append(data[0])

    return project_options
