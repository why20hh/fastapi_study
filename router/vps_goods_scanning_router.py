from fastapi import APIRouter, BackgroundTasks
from common.mysql_connect import get_db_session
from utils.user_jwt import get_current_user
from models.vps_goods_scanning import VpsGoodsScanningModels
from models.background_tasks_manager import TaskManager
from crud.vps_goods_scanning_curd import scanning_goods_curd
from sqlalchemy import asc, delete
from uuid import uuid4
import asyncio
from time import sleep
from utils.middleware import logger

vps_scanning_router = APIRouter(prefix='/vps_goods_scan/api', tags=['商品信息扫描'])
task_manager = TaskManager()


@vps_scanning_router.get('/', summary="查询所有数据")
async def get_vps_scanning_data():
    db = get_db_session()
    all_result = db.query(VpsGoodsScanningModels).order_by(asc(VpsGoodsScanningModels.vps_service_name)).all()
    return all_result


@vps_scanning_router.post('/scan_goods', summary="扫描指定网址")
async def scan_goods(background_tasks: BackgroundTasks, scan_url: str, num_of_scan: int):
    task_id = str(uuid4())

    async def scan_task():
        db = get_db_session()
        try:
            scanning_result = await scanning_goods_curd(db, scan_url, num_of_scan)
            logger.info(scanning_result)
        except Exception as e:
            logger.info(f"An error occurred: {e}")
        task_manager.update_task_status(task_id, "completed")  # 完成时更新状态
        # 这里可以添加日志或其他处理逻辑，但通常不直接返回结果，因为它在后台运行

    # 直接使用传入的background_tasks，无需再次实例化
    background_tasks.add_task(scan_task)
    task_manager.add_task(task_id, {"scan_url": scan_url, "num_of_scan": num_of_scan})

    return {"task_id": task_id, "message": "扫描任务已启动，将在后台执行"}


@vps_scanning_router.get("/get_tasks", summary="查询后台任务状态")
async def get_tasks():
    return task_manager.get_tasks()


@vps_scanning_router.delete('/delete_all_goods_data', summary="删除当前所有数据")
async def delete_all_goods_data():
    db = get_db_session()
    delete_statement = delete(VpsGoodsScanningModels)
    db.execute(delete_statement)
    db.commit()
    return {"message": "All Goods Data Deleted Successfully"}
