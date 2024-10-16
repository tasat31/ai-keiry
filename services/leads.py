import pandas as pd
from datetime import datetime
from settings import logger
from resources.keiry_db import db_read, db_write
from typing import List
from app.types.lead import Lead

def find(id=None):

    sql = """
            SELECT
                id,
                name,
                entity,
                postal_no,
                prefecture,
                city,
                address,
                url,
                tel,
                segment,
                cluster,
                trade_status,
                rank,
                first_contacted_at,
                first_contacted_media,
                last_contacted_at,
                description,
                partner_name,
                partner_role,
                partner_tel_1,
                partner_tel_2,
                partner_mail_address,
                created_at,
                updated_at
            FROM leads
            WHERE id = '%s'
        """ % (id)

    logger.debug(sql)
    res = db_read(sql)

    data = res.fetchone()

    if data is None:
        return None

    return Lead(
        id=data[0],
        name=data[1],
        entity=data[2],
        postal_no=data[3],
        prefecture=data[4],
        city=data[5],
        address=data[6],
        url=data[7],
        tel=data[8],
        segment=data[9],
        clusterr=data[10],
        trade_status=data[11],
        rank=data[12],
        first_contacted_at=data[13],
        first_contacted_media=data[14],
        last_contacted_at=data[15],
        description=data[16],
        partner_name=data[17],
        partner_role=data[18],
        partner_tel_1=data[19],
        partner_tel_2=data[20],
        partner_mail_address=data[21],
        created_at=data[22],
        updated_at=data[23],
    )

def list(segment=None, cluster=None, last_contacted_at_from=None, last_contacted_at_to=None, show_deleted=False):
    where = ''

    if segment is not None:
        where = "segment = '%s'" % segment

    if cluster is not None:
        cluster_condition = "cluster = '%s'" % cluster
        if where != '':
            where = where + " AND %s" % cluster_condition
        else:
            where = cluster_condition

    if last_contacted_at_from is not None and last_contacted_at_to is not None:
        last_contacted_at_condition = "last_contacted_at BETWEEN '%s' AND '%s'" % (last_contacted_at_from.strftime('%Y-%m-%d'), last_contacted_at_to.strftime('%Y-%m-%d'))
        if where != '':
            where = where + " AND %s" % last_contacted_at_condition
        else:
            where = last_contacted_at_condition

    if show_deleted == False:
        if where != '':
            where = where + " AND trade_status <> '削除'"
        else:
            where = "trade_status <> '削除'"

    if where != '':
        where = "WHERE %s" % where

    sql = """
            SELECT
                id,
                name,
                entity,
                postal_no,
                prefecture,
                city,
                address,
                url,
                tel,
                segment,
                cluster,
                trade_status,
                rank,
                first_contacted_at,
                first_contacted_media,
                last_contacted_at,
                description,
                partner_name,
                partner_role,
                partner_tel_1,
                partner_tel_2,
                partner_mail_address,
                created_at,
                updated_at
             FROM leads
             %s
        """ % where

    logger.debug(sql)
    res = db_read(sql)

    leads = []
    for data in res.fetchall():
        leads.append(
            Lead(
                id=data[0],
                name=data[1],
                entity=data[2],
                postal_no=data[3],
                prefecture=data[4],
                city=data[5],
                address=data[6],
                url=data[7],
                tel=data[8],
                segment=data[9],
                cluster=data[10],
                trade_status=data[11],
                rank=data[12],
                first_contacted_at=data[13],
                first_contacted_media=data[14],
                last_contacted_at=data[15],
                description=data[16],
                partner_name=data[17],
                partner_role=data[18],
                partner_tel_1=data[19],
                partner_tel_2=data[20],
                partner_mail_address=data[21],
                created_at=data[22],
                updated_at=data[23],
            )
        )
    
    return leads

def entry(
        lead: Lead = None
    ):

    if (lead is None):
        return

    sql = """
        INSERT INTO leads(
            name,
            entity,
            postal_no,
            prefecture,
            city,
            address,
            url,
            tel,
            segment,
            cluster,
            trade_status,
            rank,
            first_contacted_at,
            first_contacted_media,
            last_contacted_at,
            description,
            partner_name,
            partner_role,
            partner_tel_1,
            partner_tel_2,
            partner_mail_address,
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
            '%s',
            '%s',
            '%s',
            '%s',
            '%s',
            %s,
            '%s',
            %s,
            '%s',
            '%s',
            '%s',
            '%s',
            '%s',
            '%s',
            '%s',
            '%s'
        )
            """ % (
            lead.name,
            lead.entity,
            lead.postal_no.replace('-', ''),
            lead.prefecture,
            lead.city,
            lead.address,
            lead.url,
            lead.tel,
            lead.segment,
            lead.cluster,
            lead.trade_status,
            lead.rank,
            "'" + lead.first_contacted_at.strftime('%Y-%m-%d') + "'" if lead.first_contacted_at is not None else 'NULL',
            lead.first_contacted_media,
            "'" + lead.last_contacted_at.strftime('%Y-%m-%d') + "'" if lead.last_contacted_at is not None else 'NULL' ,
            lead.description,
            lead.partner_name,
            lead.partner_role,
            lead.partner_tel_1,
            lead.partner_tel_2,
            lead.partner_mail_address,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )

    logger.debug(sql)
    db_write(sql)

def update(
        lead: Lead = None
    ):

    if (lead is None):
        return

    sql = """
        UPDATE leads
        SET
            name = '%s',
            entity = '%s',
            postal_no = '%s',
            prefecture = '%s',
            city = '%s',
            address = '%s',
            url = '%s',
            tel = '%s',
            segment = '%s',
            cluster = '%s',
            trade_status = '%s',
            rank = '%s',
            first_contacted_at = %s,
            first_contacted_media = '%s',
            last_contacted_at = %s,
            description = '%s',
            partner_name = '%s',
            partner_role = '%s',
            partner_tel_1 = '%s',
            partner_tel_2 = '%s',
            partner_mail_address = '%s',
            updated_at = '%s'
        WHERE id = %s
    """ % (
            lead.name,
            lead.entity,
            lead.postal_no.replace('-', ''),
            lead.prefecture,
            lead.city,
            lead.address,
            lead.url,
            lead.tel,
            lead.segment,
            lead.cluster,
            lead.trade_status,
            lead.rank,
            "'" + lead.first_contacted_at.strftime('%Y-%m-%d') + "'" if lead.first_contacted_at is not None else 'NULL',
            lead.first_contacted_media,
            "'" + lead.last_contacted_at.strftime('%Y-%m-%d') + "'" if lead.last_contacted_at is not None else 'NULL' ,
            lead.description,
            lead.partner_name,
            lead.partner_role,
            lead.partner_tel_1,
            lead.partner_tel_2,
            lead.partner_mail_address,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            lead.id,
        )

    logger.debug(sql)
    db_write(sql)

def delete(id=None):
    if (id is None):
        return

    sql = """
            DELETE
            FROM leads
            WHERE id='%s'
        """ % (id)

    logger.debug(sql)
    db_write(sql)

def bulk_entry(df: pd.DataFrame):
    try:
        csv_records = df.to_csv().split('\n')
        for csv_rec in csv_records[1:]:
            data = csv_rec.split(',')
            if len(data) >= 22:
                lead = Lead(
                    name=data[2],
                    segment=data[3],
                    cluster=data[4],
                    trade_status=data[5],
                    rank=data[6],
                    first_contacted_at=datetime.strptime(data[7], '%Y-%m-%d'),
                    first_contacted_media=data[8],
                    last_contacted_at=datetime.strptime(data[9], '%Y-%m-%d'),
                    description=data[10],
                    entity=data[11],
                    postal_no=data[12],
                    prefecture=data[13],
                    city=data[14],
                    address=data[15],
                    url=data[16],
                    tel=data[17],
                    partner_name=data[18],
                    partner_role=data[19],
                    partner_tel_1=data[20],
                    partner_tel_2=data[21],
                    partner_mail_address=data[22],
                )

                entry(lead=lead)
        return {"message": "Uploaded successfully."}
    except Exception as e:
        return {"message": f"Error: {e}"}

def bulk_update(df: pd.DataFrame):
    try:
        csv_records = df.to_csv().split('\n')
        for csv_rec in csv_records[1:]:
            data = csv_rec.split(',')
            if len(data) >= 23:
                lead = Lead(
                    name=data[2],
                    segment=data[3],
                    cluster=data[4],
                    trade_status=data[5],
                    rank=data[6],
                    first_contacted_at=datetime.strptime(data[7], '%Y-%m-%d'),
                    first_contacted_media=data[8],
                    last_contacted_at=datetime.strptime(data[9], '%Y-%m-%d'),
                    description=data[10],
                    entity=data[11],
                    postal_no=data[12],
                    prefecture=data[13],
                    city=data[14],
                    address=data[15],
                    url=data[16],
                    tel=data[17],
                    partner_name=data[18],
                    partner_role=data[19],
                    partner_tel_1=data[20],
                    partner_tel_2=data[21],
                    partner_mail_address=data[22],
                    id=data[23],
                )

                update(lead=lead)
        return {"message": "Uploaded successfully."}
    except Exception as e:
        return {"message": f"Error: {e}"}

def lead_options():
    sql = """
            SELECT
                name,
                entity,
                updated_at
             FROM leads
             GROUP BY name, entity, updated_at
             ORDER BY updated_at
        """

    logger.debug(sql)
    res = db_read(sql)

    lead_options = []
    for data in res.fetchall():
        lead_options.append(
            data[0]
        )

    return lead_options

def lead_id_name_options():
    sql = """
            SELECT
                id,
                name,
                updated_at
             FROM leads
             GROUP BY name, updated_at
             ORDER BY updated_at
        """

    logger.debug(sql)
    res = db_read(sql)

    lead_id_name_options = []
    for data in res.fetchall():
        lead_id_name_options.append({
            "id": data[0],
            "name": data[1]
        })

    return lead_id_name_options

def cluster_options():
    sql = """
            SELECT
                cluster
             FROM leads
             GROUP BY cluster
        """

    logger.debug(sql)
    res = db_read(sql)

    cluster_options = []
    for data in res.fetchall():
        cluster_options.append(data[0])

    return cluster_options
