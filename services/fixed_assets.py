import pandas as pd
from datetime import datetime
from settings import logger
from resources.keiry_db import db_read, db_write
from app.types.fixed_asset import FixedAsset
from dateutil.relativedelta import relativedelta
from utils.datetime import list_by_month
from collections import OrderedDict
from services.kittings import fiscal_term_settings

def find(id=None):

    sql = """
            SELECT
                id,
                name,
                launched_at,
                obtained_at,
                obtained_type,
                item,
                amount,
                structure_or_use,
                details,
                depreciating_years,
                depreciation_expense_total_at_last_fiscal_year,
                location,
                remark,
                created_at,
                updated_at
            FROM fixed_assets
            WHERE id = '%s'
        """ % (id)

    logger.debug(sql)
    res = db_read(sql)

    data = res.fetchone()

    if data is None:
        return None

    return FixedAsset(
        id=data[0],
        name=data[1],
        launched_at=data[2],
        obtained_at=data[3],
        obtained_type=data[4],
        item=data[5],
        amount=data[6],
        structure_or_use=data[7],
        details=data[8],
        depreciating_years=data[9],
        depreciation_expense_total_at_last_fiscal_year=data[10],
        location=data[11],
        remark=data[12],
        created_at=data[13],
        updated_at=data[14],
    )

def list():
    sql = """
            SELECT
                id,
                name,
                launched_at,
                obtained_at,
                obtained_type,
                item,
                amount,
                structure_or_use,
                details,
                depreciating_years,
                depreciation_expense_total_at_last_fiscal_year,
                location,
                remark,
                created_at,
                updated_at
             FROM fixed_assets
             ORDER BY obtained_at
        """

    logger.debug(sql)
    res = db_read(sql)

    fixed_assets = []
    for data in res.fetchall():
         fixed_assets.append(
            FixedAsset(
                id=data[0],
                name=data[1],
                launched_at=data[2],
                obtained_at=data[3],
                obtained_type=data[4],
                item=data[5],
                amount=data[6],
                structure_or_use=data[7],
                details=data[8],
                depreciating_years=data[9],
                depreciation_expense_total_at_last_fiscal_year=data[10],
                location=data[11],
                remark=data[12],
                created_at=data[13],
                updated_at=data[14],
            )
        )
    
    return fixed_assets

def entry(
        fixed_asset: FixedAsset = None
    ):

    if (fixed_asset is None):
        return

    sql = """
        INSERT INTO fixed_assets(
            name,
            launched_at,
            obtained_at,
            obtained_type,
            item,
            amount,
            structure_or_use,
            details,
            depreciating_years,
            depreciation_expense_total_at_last_fiscal_year,
            location,
            remark,
            created_at,
            updated_at
        ) VALUES(
            '%s',
            '%s',
            '%s',
            '%s',
            '%s',
            %s,
            '%s',
            '%s',
            %s,
            %s,
            '%s',
            '%s',
            '%s',
            '%s'
        )
            """ % (
            fixed_asset.name,
            fixed_asset.launched_at.strftime('%Y-%m-%d'),
            fixed_asset.obtained_at.strftime('%Y-%m-%d'),
            fixed_asset.obtained_type,
            fixed_asset.item,
            fixed_asset.amount,
            fixed_asset.structure_or_use,
            fixed_asset.details,
            fixed_asset.depreciating_years,
            fixed_asset.depreciation_expense_total_at_last_fiscal_year,
            fixed_asset.location,
            fixed_asset.remark,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )

    logger.debug(sql)
    db_write(sql)

def update(
        fixed_asset: FixedAsset = None
    ):

    if (fixed_asset is None):
        return

    sql = """
        UPDATE fixed_assets
        SET
            name               = '%s',
            launched_at        = '%s',
            obtained_at        = '%s',
            obtained_type      = '%s',
            item               = '%s',
            amount             = %s,
            structure_or_use   = '%s',
            details            = '%s',
            depreciating_years = %s,
            depreciation_expense_total_at_last_fiscal_year = %s,
            location           = '%s',
            remark             = '%s',
            updated_at         = '%s'
        WHERE id = %s
    """ % (
            fixed_asset.name,
            fixed_asset.launched_at.strftime('%Y-%m-%d'),
            fixed_asset.obtained_at.strftime('%Y-%m-%d'),
            fixed_asset.obtained_type,
            fixed_asset.item,
            fixed_asset.amount,
            fixed_asset.structure_or_use,
            fixed_asset.details,
            fixed_asset.depreciating_years,
            fixed_asset.depreciation_expense_total_at_last_fiscal_year,
            fixed_asset.location,
            fixed_asset.remark,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            fixed_asset.id,
        )

    logger.debug(sql)
    db_write(sql)

def delete(id=None):
    if (id is None):
        return

    sql = """
            DELETE
            FROM fixed_assets
            WHERE id=%s
        """ % (id)

    logger.debug(sql)
    db_write(sql)

def bulk_update(df: pd.DataFrame):
    try:
        csv_records = df.to_csv().split('\n')
        for csv_rec in csv_records[1:]:
            data = csv_rec.split(',')
            if len(data) >= 15:
                fixed_asset = FixedAsset(
                    name=data[2],
                    item=data[3],
                    launched_at=data[4],
                    obtained_at=data[5],
                    obtained_type=data[6],
                    amount=data[7],
                    structure_or_use=data[8],
                    details=data[9],
                    depreciating_years=data[10],
                    depreciation_expense_total_at_last_fiscal_year=data[12],
                    location=data[14],
                    remark=data[15],
                    id=data[16],
                )
                update(fixed_asset=fixed_asset)

        return {"message": "Uploaded successfully."}
    except Exception as e:
        return {"message": f"Error: {e}"}

def bulk_delete(df: pd.DataFrame):
    for index, row in df.iterrows():
        data = row.to_dict()
        delete(id=int(data["id"]))

def fixed_asset_options():
    sql = """
        SELECT
            name
        FROM items
        WHERE category = 'FA'
        ORDER BY id
    """

    logger.debug(sql)
    res = db_read(sql)

    fixed_asset_options = []
    for data in res.fetchall():
        fixed_asset_options.append(data[0])

    return fixed_asset_options

# 定額法
def calculate_straight_line_method(obtained_at=datetime.now(), depreciating_years=1, amount=0, depreciation_expense_total_at_last_fiscal_year=0) -> dict:
    (fiscal_start_date, fiscal_end_date, fiscal_term) = fiscal_term_settings()
    depreciation_start_date = obtained_at
    depreciation_end_date = obtained_at + relativedelta(years=depreciating_years) - relativedelta(months=1)
    year_months = list_by_month(
        start_date=depreciation_start_date,
        end_date=depreciation_end_date
    )

    depreciation_expense_per_month = int(amount / len(year_months) + 0.5)
    depreciation_expenses_by_fiscal_year = OrderedDict()
    depreciation_expense_subtotal = 0
    depreciation_expense_total = 0
    depreciation_expense_total_at_last_fiscal_year_calculated = 0

    for year_month in sorted(year_months):
        if year_month.month == fiscal_end_date.month:
            (fiscal_term_year, fiscal_term_month) = (year_month.year, year_month.month)
            fiscal_term_key = f"{fiscal_term_year}年{fiscal_term_month:02}月期"
            depreciation_expenses_by_fiscal_year[fiscal_term_key] = depreciation_expense_subtotal + depreciation_expense_per_month
            depreciation_expense_total += depreciation_expenses_by_fiscal_year[fiscal_term_key]
            if (year_month.year < fiscal_end_date.year):
                depreciation_expense_total_at_last_fiscal_year_calculated += depreciation_expenses_by_fiscal_year[fiscal_term_key]

            depreciation_expense_subtotal = 0
        else:
            depreciation_expense_subtotal += depreciation_expense_per_month
    
    if amount > depreciation_expense_total:
        fiscal_term_key = f"{fiscal_term_year + 1}年{fiscal_term_month:02}月期"
        depreciation_expenses_by_fiscal_year[fiscal_term_key] = amount - depreciation_expense_total + (depreciation_expense_total_at_last_fiscal_year_calculated - depreciation_expense_total_at_last_fiscal_year)

    return {
        "depreciation_start_date": depreciation_start_date,
        "depreciation_end_date": depreciation_end_date,
        "depreciation_expense_per_month": depreciation_expense_per_month,
        "depreciation_expenses_by_fiscal_year": depreciation_expenses_by_fiscal_year,
    }
