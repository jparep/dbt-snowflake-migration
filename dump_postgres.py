import os
import subprocess
from dotenv import load_dotenv
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def validate_env_vars(required_vars):
    """Validate required environment variables."""
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

def dump_postgres():
    """Dump PostgreSQL database to a file."""
    # Ensure the data directory exists
    dump_dir = "data"
    os.makedirs(dump_dir, exist_ok=True)

    # Create a timestamped file name for the dump
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dump_file = os.path.join(dump_dir, f"postgres_backup_{timestamp}.sql")

    try:
        # Command to dump PostgreSQL database
        command = [
            "pg_dump",
            "--host", os.getenv("POSTGRES_HOST"),
            "--port", os.getenv("POSTGRES_PORT"),
            "--username", os.getenv("POSTGRES_USER"),
            "--dbname", os.getenv("POSTGRES_DATABASE"),
            "--file", dump_file,
            "--no-password"
        ]

        # Run the command with the password in the environment
        subprocess.run(
            command,
            check=True,
            env={**os.environ, "PGPASSWORD": os.getenv("POSTGRES_PASSWORD")},
        )
        logger.info(f"Database dump successful: {dump_file}")
        return dump_file
    except subprocess.CalledProcessError as e:
        logger.error(f"Error during database dump: {e}")
        return None

if __name__ == "__main__":
    # Validate required environment variables
    required_env_vars = [
        "POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_USER",
        "POSTGRES_PASSWORD", "POSTGRES_DATABASE"
    ]
    try:
        validate_env_vars(required_env_vars)
        dump_postgres()
    except ValueError as e:
        logger.error(e)
