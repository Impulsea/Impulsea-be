import psycopg2

from pathlib import Path
import logging
import os


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def execute_sql_file(sql_file_path: str, connection_params: dict) -> None:
    # Read SQL file content
    with open(sql_file_path, "r") as file:
        sql_script = file.read()

    try:
        # Establish a connection to the PostgreSQL database
        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()

        # Execute the SQL script
        cursor.execute(sql_script)

        # Commit the changes
        connection.commit()

        logger.info("SQL script executed successfully.")

        cursor.close()
        connection.close()
    except (psycopg2.Error, Exception) as e:
        logger.error(f"Error executing SQL script: {e}")


def main() -> None:
    # Replace these parameters with your own database connection details
    connection_parameters = {
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
    }

    # Input the path to your SQL file
    sql_file_path = input("Enter the path to the SQL file: ")

    # Check if the file exists
    if not Path(sql_file_path).is_file():
        logger.error(f"Error: The file '{sql_file_path}' does not exist.")
    else:
        # Execute the SQL file
        execute_sql_file(sql_file_path, connection_parameters)


if __name__ == "__main__":
    main()
