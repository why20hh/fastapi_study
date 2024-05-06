from fastapi import APIRouter, Form, HTTPException, status
from fastapi.responses import JSONResponse
from utils.user_jwt import create_access_token
from crud.user_curd import authenticate_user
from common.mysql_connect import get_db_session

login_router = APIRouter(tags=['用户登录'])


@login_router.post("/token")
async def login(username: str = Form(...), password: str = Form(...)):
    # 在此处验证用户名和密码，生成访问令牌
    db = get_db_session()
    is_valid_credentials = authenticate_user(username, password, db)

    if not is_valid_credentials:
        # 如果用户名不存在或者密码错误，返回相应的错误信息
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or Password is incorrect"
        )
    user_credentials = {"username": username, "password": password}

    # 在此处验证用户名和密码，生成访问令牌
    access_token = create_access_token(data=user_credentials)
    return {"access_token": access_token, "token_type": "bearer"}

route_config = [
    {
        "path": "/dashboard",
        "name": "Dashboard",
        "component": "@/views/DashboardView.vue",
        "icon": "<el-icon><DataBoard /></el-icon>"
    },
    {
        "path": "/settings",
        "name": "Settings",
        "component": "@/views/SettingsView.vue",
        "icon": "<el-icon><Setting /></el-icon>"
    }
]


@login_router.get("/get_apis", summary="获取路由信息")
async def get_apis():
    return JSONResponse(content=route_config)
