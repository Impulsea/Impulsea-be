import os
import re
import logging
import sqlparse
import psycopg2

from config import (
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
)


PATH = "src/db/migrations/"
MIGRATION_FILE_FORMAT = r"^\d+_.*\.sql$"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_megrations():
    migrations = [mig for mig in os.listdir(PATH) if re.match(MIGRATION_FILE_FORMAT, mig)]
    migrations.sort()
    return migrations


def create_migrations_table(connection, cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS migrations (name TEXT);")
    connection.commit()


def migration_executed(cursor, migration_name):
    cursor.execute(f"SELECT name FROM migrations WHERE name = '{migration_name}';")
    return len(cursor.fetchall()) > 0


def insert_migration(connection, cursor, migration_name):
    cursor.execute(f'''INSERT INTO migrations (name) VALUES ('{migration_name}')''')
    connection.commit()


def execute_migration(cursor, connection, migration):
    migration_file = os.path.join(PATH, migration)

    with open(migration_file, 'r') as f:
        migration_statements = f.read()

    statements = sqlparse.split(migration_statements)
    statements = [sqlparse.format(statement, strip_comments=True) for statement in statements]

    for statement in statements:
        if (len(statement.strip()) == 0):
            continue

        logging.info(statement)
        cursor.execute(statement)
        connection.commit()

    return True


def main():

    connection = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = connection.cursor()
    logging.info('Connected.')

    create_migrations_table(connection=connection, cursor=cursor)

    migrations = get_megrations()

    for migration_name in migrations:
        if not os.path.isfile(os.path.join(PATH, migration_name)):
            logging.info(f"Skipped: {migration_name}")
            continue

        if migration_executed(cursor, migration_name):
            logging.info(f"Migration {migration_name} is already ran")
            continue

        logging.info(f"Running migration: {migration_name}")
        execute_migration(cursor=cursor, connection=connection, migration=migration_name)
        insert_migration(connection=connection, cursor=cursor, migration_name=migration_name)

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
