from settings import SQLALCHEMY_DATABASE_URL, SQLALCHEMY_DATABASE_URL_ASYNC
from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def get_db_context():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db is not None:
            db.close()


# async def get_async_db_context():
#     async with AsyncSessionLocal() as async_db:
#         yield async_db

engine = create_engine(SQLALCHEMY_DATABASE_URL)
# async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL_ASYNC)

metadata = MetaData().create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# AsyncSessionLocal = async_sessionmaker(async_engine, autocommit=False, autoflush=False)

Base = declarative_base()
