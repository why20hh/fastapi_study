from sqlalchemy import Column, Integer, String, DATETIME, func, Text
from common.mysql_connect import Base
from pydantic import BaseModel


class VpsGoodsScanningModels(Base):
    __tablename__ = "vps_goods_scanning"
    vps_goods_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    vps_goods_name = Column(String(255))
    vps_goods_description = Column(String(255))
    vps_price_monthly = Column(String(255), default=None)
    vps_price_quarterly = Column(Text(length=16777215))
    vps_price_annually = Column(String(255), default=None)
    vps_buy_link = Column(String(255), default=None)
    vps_service_name = Column(String(255), default=None)
    vps_data_created_time = Column(DATETIME, default=func.now())
    vps_data_last_edit_time = Column(DATETIME, default=None)

# class VpsBuyModel(BaseModel):
#     template_name: str = ""
#     login_address: str = ""
#     add_cart_address: str = ""
#     template_username: str = ""
#     template_passwd: str = ""
#     template_payment: str = ""
