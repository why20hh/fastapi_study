from sqlalchemy import Column, Integer, String, DATETIME, func
from common.mysql_connect import Base
from pydantic import BaseModel


class VpsTemplateModel(Base):
    __tablename__ = "vps_buy_template"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    template_name = Column(String(255), primary_key=True, index=True)
    login_address = Column(String(255), primary_key=True, index=True)
    add_cart_address = Column(String(255), primary_key=True, index=True)
    template_username = Column(String(255), default=None)
    template_passwd = Column(String(255), default=None)
    template_payment = Column(String(255), default=None)
    template_created_time = Column(DATETIME, default=func.now())
    last_edit_time = Column(DATETIME, default=None)


class VpsBuyModel(BaseModel):
    template_name: str = ""
    login_address: str = ""
    add_cart_address: str = ""
    template_username: str = ""
    template_passwd: str = ""
    template_payment: str = ""
