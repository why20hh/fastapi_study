import logging
from fastapi import FastAPI, Request
from datetime import datetime

# 创建日志记录器
logger = logging.getLogger("my_logger")  # 创建一个新的日志记录器，而不是使用 "uvicorn"
logger.setLevel(logging.DEBUG)

# 创建文件处理器
file_handler = logging.FileHandler('./log/app.log')
file_handler.setLevel(logging.DEBUG)

# 创建流处理器
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

# 创建格式器
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# 添加格式器到处理器
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# 添加处理器到日志记录器
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


async def log_request(request: Request, call_next):
    start_time = datetime.now()

    logger.info(f"Received request at {start_time}: {request.method} - {request.url.path}")

    if "content-length" in request.headers and int(request.headers["content-length"]) > 0:
        try:
            request_body = await request.body()
            logger.info(f"Request body: {request_body.decode()}")
        except Exception as e:
            logger.error(f"Failed to read request body: {e}")

    response = await call_next(request)

    return response
