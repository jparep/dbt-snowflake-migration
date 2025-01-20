import os
import subprocess
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

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
            "--file", dump_file
        ]

        # Run the command with the password in the environment
        subprocess.run(
            command,
            check=True,
            env={**os.environ, "PGPASSWORD": os.getenv("POSTGRES_PASSWORD")},
        )
        print(f"Database dump successful: {dump_file}")
        return dump_file
    except subprocess.CalledProcessError as e:
        print(f"Error during database dump: {e}")
        return None

if __name__ == "__main__":
    dump_postgres()