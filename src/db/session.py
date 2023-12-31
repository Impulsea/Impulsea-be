from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session, sessionmaker

from config import POSTGRES_URI


def create_sessionmaker(postgres_uri: str) -> sessionmaker[Session]:
    engine = create_engine(url=postgres_uri)
    return sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False
    )


session_maker = create_sessionmaker(POSTGRES_URI)
