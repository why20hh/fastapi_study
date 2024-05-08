from fastapi import APIRouter, Depends, HTTPException
from common.mysql_connect import get_db_session
from utils.user_jwt import get_current_user
from models.vps_buy_models import VpsBuyModel, VpsTemplateModel
from crud.vps_buy_curd_template import add_template, update_template, delete_template
from crud.vps_buy_curd_request import get_data_req

vps_buy_router = APIRouter(prefix='/vps_buy/api', tags=['VPS购买'])


# 返回首页html
@vps_buy_router.get("/", summary="首页")
@vps_buy_router.get("/index", summary="首页")
async def vps_buy_main_page(current_user: dict = Depends(get_current_user)):
    pass


# 返回模板管理html
@vps_buy_router.get("/template", summary="下单模板管理")
async def order_template_management(current_user: dict = Depends(get_current_user)):
    pass


@vps_buy_router.post("/add_template", summary="添加模板")
async def add_vps_buy_template(template_data: VpsBuyModel, current_user: dict = Depends(get_current_user)):
    db = get_db_session()
    add_template_result = add_template(db, template_data)
    return add_template_result


@vps_buy_router.put("/update_template/{template_id}", summary="修改模板")
async def update_vps_buy_template(template_id: int, template_data: VpsBuyModel,
                                  current_user: dict = Depends(get_current_user)):
    db = get_db_session()
    update_template_result = update_template(db, template_id, template_data)
    return update_template_result


@vps_buy_router.delete("/delete_template/{template_id}", summary="删除模板")
async def delete_vps_buy_template(template_id: int, current_user: dict = Depends(get_current_user)):
    db = get_db_session()
    delete_template_result = delete_template(db, template_id)
    return delete_template_result


@vps_buy_router.post("/login", summary="立即登录")
async def login_in_now(template_data: VpsBuyModel, current_user: dict = Depends(get_current_user)):
    get_data_req(template_data)


@vps_buy_router.post("/no_login_now", summary="暂不登录")
async def login_no_now(current_user: dict = Depends(get_current_user)):
    pass


@vps_buy_router.get("/refresh_sessions", summary="刷新Session")
async def refresh_sessions(current_user: dict = Depends(get_current_user)):
    pass


@vps_buy_router.post("/order_now", summary="立即下单")
async def order_now(current_user: dict = Depends(get_current_user)):
    pass


@vps_buy_router.post("/order_in_background", summary="后台下单")
async def order_later(current_user: dict = Depends(get_current_user)):
    pass


@vps_buy_router.get("/query_background_tasks", summary="查询后台任务")
async def query_background_tasks(current_user: dict = Depends(get_current_user)):
    pass


@vps_buy_router.delete("/delete_background_tasks", summary="删除后台任务")
async def delete_background_tasks(current_user: dict = Depends(get_current_user)):
    pass
