from fastapi import APIRouter, HTTPException, Depends
from common.mysql_connect import get_db_session
from crud.user_curd import get_user, create_user, update_user, delete_user
from models.user_models import UserInfo
from models.response_model import ResponseModel
from utils.user_jwt import get_current_user

edit_user_router = APIRouter(prefix='/user', tags=['用户管理'])


@edit_user_router.get("/{get_user_name}", summary='查询用户')
async def read_user(get_user_name: str, current_user: dict = Depends(get_current_user)):
    db = get_db_session()
    user = get_user(db, get_user_name)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@edit_user_router.post("/create_user", summary='添加用户')
async def create_new_user(user_data: UserInfo):
    db = get_db_session()
    user = create_user(db, user_data)
    return user


@edit_user_router.put("/{get_user_name}", summary='修改用户')
async def update_existing_user(get_user_name: str, user_data: UserInfo, current_user: dict = Depends(get_current_user)):
    db = get_db_session()
    user = get_user(db, get_user_name)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = update_user(db, user, user_data)
    return updated_user


@edit_user_router.delete("/{get_user_name}", response_model=ResponseModel, summary='删除')
async def delete_existing_user(get_user_name: str, current_user: dict = Depends(get_current_user)):
    db = get_db_session()
    user = get_user(db, get_user_name)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    delete_user(db, user)
    data = {"message": "User deleted successfully"}
    return {"data": data}
