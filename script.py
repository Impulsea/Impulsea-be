from pathlib import Path

import psycopg2


def execute_sql_file(sql_file_path, connection_params):
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

        print("SQL script executed successfully.")

    except (psycopg2.Error, Exception) as e:
        print(f"Error executing SQL script: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def main() -> None:
    # Replace these parameters with your own database connection details
    connection_parameters = {
        "dbname": "your_database_name",
        "user": "your_username",
        "password": "your_password",
        "host": "your_host",
        "port": "your_port",
    }

    # Input the path to your SQL file
    sql_file_path = input("Enter the path to the SQL file: ")

    # Check if the file exists
    if not Path(sql_file_path).is_file():
        print(f"Error: The file '{sql_file_path}' does not exist.")
    else:
        # Execute the SQL file
        execute_sql_file(sql_file_path, connection_parameters)


if __name__ == "__main__":
    main()
