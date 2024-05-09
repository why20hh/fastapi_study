from fastapi import FastAPI, Request
from common.mysql_connect import create_tables
from starlette.middleware.base import BaseHTTPMiddleware
from utils.middleware import log_request
from router.user_edit import edit_user_router
from router.user_login import login_router
from router.vps_edit import edit_vps_router
from router.vps_buy import vps_buy_router
from router.vps_goods_scanning_router import vps_scanning_router
from async_timeout import timeout

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 设置为 * 表示允许所有来源
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # 允许的 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)
# class TimeoutMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request, call_next):
#         async with timeout(10):  # 设置超时时间为 10 秒
#             response = await call_next(request)
#         return response


app.middleware("http")(log_request)
app.include_router(login_router)
app.include_router(edit_user_router)
app.include_router(edit_vps_router)
app.include_router(vps_buy_router)
app.include_router(vps_scanning_router)
# app.add_middleware(TimeoutMiddleware)

if __name__ == '__main__':
    import uvicorn

    create_tables()
    uvicorn.run('main:app', host='0.0.0.0', port=39234, reload=True)
