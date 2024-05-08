import datetime
from sqlalchemy.orm import Session
from models.vps_buy_models import VpsBuyModel, VpsTemplateModel
from fastapi import HTTPException
from datetime import datetime


def add_template(db: Session, template_data: VpsBuyModel):
    add_template_data = VpsTemplateModel(
        template_name=template_data.template_name,
        login_address=template_data.login_address,
        add_cart_address=template_data.add_cart_address,
        template_username=template_data.template_username,
        template_passwd=template_data.template_passwd,
        template_payment=template_data.template_payment
    )
    try:
        db.add(add_template_data)
        db.commit()
        db.refresh(add_template_data)
        return {"status": "success", "data": add_template_data}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def update_template(db: Session, template_id: int, template_data: VpsBuyModel):
    # noinspection PyTypeChecker
    template_select = db.query(VpsTemplateModel).filter(VpsTemplateModel.id == template_id).first()
    if template_select:
        try:
            template_select.template_name = template_data.template_name
            template_select.login_address = template_data.login_address
            template_select.add_cart_address = template_data.add_cart_address
            template_select.template_username = template_data.template_username
            template_select.template_passwd = template_data.template_passwd
            template_select.template_payment = template_data.template_payment
            template_select.last_edit_time = datetime.now()
            db.commit()
            db.refresh(template_select)
            return {"status": "success", "data": template_data}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    else:
        raise HTTPException(status_code=404, detail="Service template not found")


def delete_template(db: Session, template_id: int):
    # noinspection PyTypeChecker
    select_template = db.query(VpsTemplateModel).filter(VpsTemplateModel.id == template_id).first()
    if select_template:
        try:
            db.delete(select_template)
            db.commit()
            return {"status": "success", "data": f"{select_template} Delete Success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    else:
        raise HTTPException(status_code=404, detail="Service template not found")
