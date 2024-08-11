from datetime import datetime
from settings import logger
from resources.keiry_db import db_read
from typing import List
from app.types.item import Item

def list():

    sql = """
            SELECT
                id,
                name,
                caption,
                category,
                display_seq,
                created_at,
                updated_at
             FROM items
             ORDER BY display_seq
        """

    logger.debug(sql)
    res = db_read(sql)

    items = []
    for data in res.fetchall():
        items.append(
            Item(
                id=data[0],
                name=data[1],
                caption=data[2],
                category=data[3],
                display_seq=data[4],
                created_at=data[5],
                updated_at=data[6],
            )
        )
    
    return items
