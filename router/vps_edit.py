from fastapi import APIRouter, Depends, HTTPException
from models.vps_models import VpsInfo
from common.mysql_connect import get_db_session
from utils.user_jwt import get_current_user
from crud.vps_curd import get_vps, create_vps, from_id_select_vpss, update_vps, delete_vps

edit_vps_router = APIRouter(prefix='/vps', tags=['VPS管理'])


@edit_vps_router.get("/select_vps", summary="查询VPS")
async def select_all_vps(current_user: dict = Depends(get_current_user)):
    db = get_db_session()
    vps = get_vps(db)
    if vps is None:
        raise HTTPException(status_code=404, detail="vps not found")
    return vps


@edit_vps_router.get("/{vps_id}", summary="根据ID查询VPS")
async def select_id_vps(vps_id: int, current_user: dict = Depends(get_current_user)):
    db = get_db_session()
    vps = from_id_select_vpss(db, vps_id)
    if vps is None:
        raise HTTPException(status_code=404, detail="Vps not found")
    return vps


@edit_vps_router.post("/create_vps", summary="添加VPS")
async def create_new_vps(vps_data: VpsInfo, current_user: dict = Depends(get_current_user)):
    db = get_db_session()
    vps = create_vps(db, vps_data)
    return vps


@edit_vps_router.put("/{vps_id}", summary="修改VPS")
async def update_existing_vps(vps_id: int, vps_data: VpsInfo, current_user: dict = Depends(get_current_user)):
    db = get_db_session()
    vps = from_id_select_vpss(db, vps_id)
    if vps is None:
        raise HTTPException(status_code=404, detail="Vps not found")
    update_vps_result = update_vps(db, vps, vps_data)
    return update_vps_result


@edit_vps_router.delete("/{vps_id}", summary="删除VPS")
async def delete_now_vps(vps_id: int, current_user: dict = Depends(get_current_user)):
    db = get_db_session()
    vps = from_id_select_vpss(db, vps_id)
    if vps is None:
        raise HTTPException(status_code=404, detail="VPS not found")
    delete_vps(db, vps)
    data = {"message": "VPS deleted successfully"}
    return {"data": data}
