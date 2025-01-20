import os
import logging
import psycopg2
import snowflake.connector
import pandas as pd
import tempfile
from dotenv import load_dotenv
from contextlib import closing
import re
import subprocess

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def validate_env_vars(required_vars):
    """Validate required environment variables and their values."""
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    # Validate Snowflake account format
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    if account and not re.match(r"^[a-zA-Z0-9]+(\.[a-zA-Z0-9\-]+)?$", account):
        raise ValueError("Invalid SNOWFLAKE_ACCOUNT format.")

def trigger_dbt():
    """Trigger dbt commands for transformations."""
    try:
        logger.info("Starting dbt transformations...")
        result = subprocess.run(["dbt", "run"], capture_output=True, text=True, check=True)
        logger.info(f"dbt run completed successfully:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during dbt run:\n{e.stderr}")
        raise

def main():
    """Main function to migrate data from PostgreSQL to Snowflake."""
    # Validate environment variables
    required_env_vars = [
        "POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DATABASE",
        "SNOWFLAKE_USER", "SNOWFLAKE_PASSWORD", "SNOWFLAKE_ACCOUNT", "SNOWFLAKE_DATABASE", "SNOWFLAKE_SCHEMA"
    ]
    validate_env_vars(required_env_vars)

    # Connect to PostgreSQL and Snowflake
    try:
        with closing(psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DATABASE")
        )) as conn_pg, closing(snowflake.connector.connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA")
        )) as conn_sf:
            logger.info("Connected to PostgreSQL and Snowflake.")

            # Extract data from PostgreSQL
            query = os.getenv("MIGRATION_QUERY", "SELECT * FROM employee")
            df = pd.read_sql(query, conn_pg)
            logger.info(f"Fetched {len(df)} rows from PostgreSQL.")

            if df.empty:
                logger.warning("No data found in PostgreSQL table.")
                return

            # Write DataFrame to CSV
            with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
                df.to_csv(temp_file.name, index=False)
                logger.info(f"Data written to {temp_file.name} for Snowflake upload.")

                # Load data into Snowflake
                cursor = conn_sf.cursor()
                try:
                    cursor.execute(f"PUT file://{temp_file.name} @%employee")
                    cursor.execute("COPY INTO employee FROM @%employee FILE_FORMAT = (TYPE = 'CSV' SKIP_HEADER = 1)")
                    logger.info("Data migration to Snowflake completed successfully.")
                finally:
                    cursor.close()
    except Exception as e:
        logger.error(f"Error during migration: {e}")
        return

    # Trigger dbt transformations
    try:
        trigger_dbt()
    except Exception as e:
        logger.error(f"Error while running dbt transformations: {e}")
    finally:
        logger.info("Migration script completed.")

if __name__ == "__main__":
    main()
