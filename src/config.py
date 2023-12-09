import os

CACHING_TIME = int(os.getenv("CACHING_TIME", "60"))

DUNE_API_KEY = os.getenv("DUNE_API_KEY", "")

DB_NAME = os.getenv("POSTGRES_DB", "")
DB_USER = os.getenv("POSTGRES_USER", "")
DB_PASSWORD = os.getenv("POSTGRES_PASS", "")
DB_HOST = os.getenv("POSTGRES_HOST", "")
DB_PORT = os.getenv("POSTGRES_PORT", "")

POSTGRES_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
