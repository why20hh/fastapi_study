from fastapi import APIRouter, Depends, HTTPException
from common.mysql_connect import get_db_session
from utils.user_jwt import get_current_user
from models.vps_goods_scanning import VpsGoodsScanningModels
from crud.vps_goods_scanning_curd import scanning_goods_curd
from sqlalchemy import asc, delete

vps_scanning_router = APIRouter(prefix='/vps_goods_scan/api', tags=['商品信息扫描'])


@vps_scanning_router.get('/', summary="查询所有数据")
async def get_vps_scanning_data():
    db = get_db_session()
    all_result = db.query(VpsGoodsScanningModels).order_by(asc(VpsGoodsScanningModels.vps_service_name)).all()
    return all_result


@vps_scanning_router.post('/scan_goods', summary="扫描指定网址")
async def scan_goods(scan_url: str, num_of_scan: int):
    db = get_db_session()
    scan_result = scanning_goods_curd(db, scan_url, num_of_scan)
    return scan_result


@vps_scanning_router.delete('/delete_all_goods_data', summary="删除当前所有数据")
async def delete_all_goods_data():
    db = get_db_session()
    delete_statement = delete(VpsGoodsScanningModels)
    db.execute(delete_statement)
    db.commit()
    return {"message": "All Goods Data Deleted Successfully"}
