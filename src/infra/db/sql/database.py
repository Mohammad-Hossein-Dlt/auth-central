from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base

Base = declarative_base()

def init_sqlite_client(
    sqlite_url: str,
) -> tuple[Session, Engine]:
    
    engine = create_engine(sqlite_url)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal(), engine

def create_sqlite_db(
    engine: Engine,
):
    Base.metadata.create_all(bind=engine)