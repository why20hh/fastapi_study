from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect
from config.settings import get_config

SQLALCHEMY_DATABASE_URL = get_config()['database']['SQLALCHEMY_DATABASE_URL']
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_tables():
    connection = engine.connect()
    inspector = inspect(connection)
    if not inspector.has_table("users"):  # 替换 "users" 为你要检查的表名
        Base.metadata.create_all(bind=engine)
    if not inspector.has_table("vps"):
        Base.metadata.create_all(bind=engine)
    if not inspector.has_table("vps_buy_template"):  # 替换 "vps_buy_template" 为你要检查的表名
        Base.metadata.create_all(bind=engine)
    if not inspector.has_table("vps_goods_scanning"):
        Base.metadata.create_all(bind=engine)


def get_db_session():
    db_session = SessionLocal()
    try:
        return db_session
    finally:
        db_session.close()
