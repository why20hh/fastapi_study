from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Date, func
from datetime import datetime

from common.mysql_connect import Base


class VpsModel(Base):
    __tablename__ = 'vps'

    vps_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    vps_name = Column(String(255), index=True)
    vps_price = Column(String(255))
    vps_next_pay = Column(Date)
    vps_pay_url = Column(String(255))
    vps_create_time = Column(Date, default=func.now())
    vps_last_modified_time = Column(Date, default=None)


class VpsInfo(BaseModel):
    vps_name: str
    vps_price: str
    vps_next_pay: datetime
    vps_pay_url: str
