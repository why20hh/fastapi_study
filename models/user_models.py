from sqlalchemy import Column, Integer, String, DATETIME, func
from common.mysql_connect import Base
from pydantic import BaseModel


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String(255), primary_key=True, index=True)
    user_email = Column(String(255))
    user_password = Column(String(255))
    registration_time = Column(DATETIME, default=func.now())
    last_modified_time = Column(DATETIME, default=None)


class UserInfo(BaseModel):
    email: str
    name: str
    password: str
