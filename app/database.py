from settings import SQLALCHEMY_DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
metadata = Base.metadata

engine = None
SessionLocal = None


def init_engine():
    global engine, SessionLocal
    if engine is None:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_context():
    if SessionLocal is None:
        init_engine()
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
