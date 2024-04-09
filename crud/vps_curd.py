import datetime
from sqlalchemy.orm import Session
from models.vps_models import VpsModel, VpsInfo


def get_vps(db: Session):
    return db.query(VpsModel).all()


def from_id_select_vpss(db: Session, vps_id: int):
    return db.query(VpsModel).filter(VpsModel.vps_id == vps_id).first()


def create_vps(db: Session, vps_data: VpsInfo):
    vps = VpsModel(vps_name=vps_data.vps_name,
                   vps_price=vps_data.vps_price,
                   vps_next_pay=vps_data.vps_next_pay,
                   vps_pay_url=vps_data.vps_pay_url)
    db.add(vps)
    db.commit()
    db.refresh(vps)
    return vps


def update_vps(db: Session, vps: VpsModel, vps_data: VpsInfo):
    vps.vps_name = vps_data.vps_name
    vps.vps_price = vps_data.vps_price
    vps.vps_next_pay = vps_data.vps_next_pay
    vps.vps_pay_url = vps_data.vps_pay_url
    vps.vps_last_modified_time = datetime.datetime.now()
    db.commit()
    db.refresh(vps)
    return vps_data


def delete_vps(db: Session, vps: VpsModel):
    db.delete(vps)
    db.commit()
