from fastapi import FastAPI, Request
from common.mysql_connect import create_tables
from starlette.middleware.base import BaseHTTPMiddleware
from utils.middleware import log_request
from router.user_edit import edit_user_router
from router.user_login import login_router
from router.vps_edit import edit_vps_router
from async_timeout import timeout

app = FastAPI()


# class TimeoutMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request, call_next):
#         async with timeout(10):  # 设置超时时间为 10 秒
#             response = await call_next(request)
#         return response


app.middleware("http")(log_request)
app.include_router(login_router)
app.include_router(edit_user_router)
app.include_router(edit_vps_router)
# app.add_middleware(TimeoutMiddleware)

if __name__ == '__main__':
    import uvicorn

    create_tables()
    uvicorn.run('main:app', host='127.0.0.1', port=39234, reload=True)
