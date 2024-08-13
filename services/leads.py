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

def list(segment=None, cluster=None, last_contacted_at_from=None, last_contacted_at_to=None):
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

def bulk_entry(csv_records: List):
    try:
        for csv_rec in csv_records:
            data = csv_rec.split(',')
            if len(data) >= 20:
                lead = Lead(
                    name=data[0],
                    entity=data[1],
                    postal_no=data[2],
                    prefecture=data[3],
                    city=data[4],
                    address=data[5],
                    url=data[6],
                    tel=data[7],
                    segment=data[8],
                    clusterr=data[9],
                    trade_status=data[10],
                    rank=data[11],
                    first_contacted_at=data[12],
                    first_contacted_media=data[13],
                    last_contacted_at=data[14],
                    description=data[15],
                    partner_name=data[16],
                    partner_role=data[17],
                    partner_tel_1=data[18],
                    partner_tel_2=data[19],
                    partner_mail_address=data[20],
                )

                entry(lead=lead)
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
            data[0] + (" 御中" if data[1] == "法人" else " 様")
        )

    return lead_options

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
