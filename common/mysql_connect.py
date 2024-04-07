from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://xSNcTXSGJCzs7jWN:xSNcTXSGJCzs7jWN@42.51.18.67/xSNcTXSGJCzs7jWN"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_tables():
    connection = engine.connect()
    inspector = inspect(connection)
    if not inspector.has_table("users"):  # 替换 "users" 为你要检查的表名
        Base.metadata.create_all(bind=engine)


def get_db_session():
    db_session = SessionLocal()
    try:
        return db_session
    finally:
        db_session.close()
