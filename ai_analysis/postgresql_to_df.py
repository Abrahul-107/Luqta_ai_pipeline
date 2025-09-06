import os
import time
import logging
import pandas as pd
from io import StringIO
from psycopg2 import pool, DatabaseError
from dotenv import load_dotenv
from contest_insights.contestInsights import generate_business_insights
from llm_call.call_llama_get_insight import get_insights_from_llm


# -------------------------------
# LOAD ENV VARIABLES
# -------------------------------
load_dotenv()

required_vars = ["DB_NAME", "DB_USER", "DB_PASS", "DB_HOST", "DB_PORT"]
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    raise EnvironmentError(f"Missing required env vars: {', '.join(missing_vars)}")

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}


# -------------------------------
# LOGGING
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger("contest_pipeline")


# -------------------------------
# DECORATOR FOR TIMING
# -------------------------------
def log_time(func):
    """Decorator to log execution time of a function"""
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.time() - start
            logger.info("⏱️ %s took %.3f seconds", func.__name__, elapsed)
    return wrapper


# -------------------------------
# CONNECTION POOL
# -------------------------------
try:
    connection_pool = pool.SimpleConnectionPool(1, 5, **DB_CONFIG)
    logger.info("Connection pool created successfully")
except DatabaseError as e:
    logger.error("Failed to create connection pool: %s", e)
    raise


# -------------------------------
# DB FETCH FUNCTION
# -------------------------------
@log_time
def fetch_data(query: str) -> pd.DataFrame:
    conn = None
    try:
        conn = connection_pool.getconn()
        buffer = StringIO()
        with conn.cursor() as cur:
            cur.copy_expert(f"COPY ({query}) TO STDOUT WITH CSV HEADER", buffer)
        buffer.seek(0)
        df = pd.read_csv(buffer)
        logger.info("Data fetched successfully (%d rows)", len(df))
        return df
    except Exception as e:
        logger.error("Error fetching data: %s", e)
        raise
    finally:
        if conn:
            connection_pool.putconn(conn)


@log_time
def run_pipeline(query: str):
    try:
        df = fetch_data(query)

        if df.empty:
            logger.warning("⚠️ Query returned no data")
            return {}

        json_for_llm = generate_business_insights(df)
        logger.info("📦 JSON prepared for LLM")

        if not isinstance(json_for_llm, dict):
            logger.error("generate_business_insights returned invalid JSON")
            return {}

        insights = get_insights_from_llm(json_for_llm)
        logger.info("Insights generated successfully")
        return insights

    except Exception as e:
        logger.error("Pipeline failed: %s", e)
        return {}


# -------------------------------
# ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    QUERY = """
    SELECT * FROM public.x2_103_contest_summary_reportingcsv
    """

    insights = run_pipeline(QUERY)
    if insights:
        logger.info("Final Insights: %s", insights)
