import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging

load_dotenv()
EQUASIS_ACCOUNT = os.environ.get("EQUASIS_ACCOUNT")
EQUASIS_PASSWORD = os.environ.get("EQUASIS_PASSWORD")

EQUASIS_BUREAU_VERITAS_ACCOUNT = os.environ.get("EQUASIS_BUREAU_VERITAS_ACCOUNT")
EQUASIS_BUREAU_VERITAS_PASSWORD = os.environ.get("EQUASIS_BUREAU_VERITAS_PASSWORD")

UPPER_LIMIT_SCRAPING_BY_ONE_BATCH = os.environ.get("UPPER_LIMIT_SCRAPING_BY_ONE_BATCH")
