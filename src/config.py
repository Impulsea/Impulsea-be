import os


DUNE_API_KEY = os.getenv("DUNE_API_KEY", "")

# get from .env
POSTGRES_URI = "postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
