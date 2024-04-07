from fastapi import FastAPI
from common.mysql_connect import create_tables
from utils.middleware import log_request
from router.user_edit import edit_user_router
from router.user_login import login_router

app = FastAPI()
app.middleware("http")(log_request)
app.include_router(login_router)
app.include_router(edit_user_router)


if __name__ == '__main__':
    import uvicorn

    create_tables()
    uvicorn.run('main:app', host='127.0.0.1', port=39234, reload=True)
