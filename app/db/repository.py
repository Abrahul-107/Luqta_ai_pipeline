import pandas as pd
from io import StringIO
from psycopg2 import pool
from app.core.config import DB_CONFIG
from app.core.logging_config import logger
from app.core.utils import log_time


class DatabaseRepository:
    def __init__(self):
        self.connection_pool = pool.SimpleConnectionPool(1, 5, **DB_CONFIG)
        logger.info("✅ Connection pool created successfully")

    @log_time
    def fetch_data(self, query: str) -> pd.DataFrame: 
        conn = None
        try:
            conn = self.connection_pool.getconn()
            buffer = StringIO()
            with conn.cursor() as cur:
                cur.copy_expert(f"COPY ({query}) TO STDOUT WITH CSV HEADER", buffer)
            buffer.seek(0)
            df = pd.read_csv(buffer)
            logger.info("📊 Data fetched successfully (%d rows)", len(df))
            return df
        finally:
            if conn:
                self.connection_pool.putconn(conn)
