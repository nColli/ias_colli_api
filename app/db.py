from dotenv import load_dotenv 
import os 
import psycopg2
import sys
import logging
load_dotenv()

database_url = os.getenv("DATABASE_URL") 
debug = os.getenv("DEBUG", "False") 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_connection():
    try:
        conn = psycopg2.connect(database_url)
        logger.info("Connected successfully")
        return conn
    except psycopg2.OperationalError as e:
        logger.error(f"Failed to connect to database: {e}")
        sys.exit(1)