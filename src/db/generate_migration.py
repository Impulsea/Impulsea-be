import argparse
import datetime


parser = argparse.ArgumentParser(
    description="Generates an empty migration file in the db folder")
parser.add_argument("name", help="the name of the migration in snake_case")

args = parser.parse_args()


def generate_migration(name):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    migration_name = "src/db/migrations/%s_%s.sql" % (timestamp, name)
    migration = open(migration_name, 'x')
    print(migration_name)
    migration.close()


if __name__ == "__main__":
    generate_migration(args.name)
