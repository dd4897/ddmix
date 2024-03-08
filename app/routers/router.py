from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config.config import STATIC,LOGPATH
from app.api.user import router as user_router
import time,random,string
import logging
from app.config.db import client
# Log config
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
fh = logging.FileHandler(filename=f'{LOGPATH}/server.log')
formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)
ch.setFormatter(formatter)
fh.setFormatter(formatter)
logger.addHandler(ch) #将日志输出至屏幕
logger.addHandler(fh) #将日志输出至文件
logger = logging.getLogger(__name__)

def init_app(app: FastAPI()):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 允许的域名列表
        allow_credentials=True,  # 允许在跨域请求中使用凭证（如Cookie）
        allow_methods=["*"],  # 允许的请求方法列表，这里使用通配符表示支持所有方法
        allow_headers=["*"],  # 允许的请求头列表，这里使用通配符表示支持所有头部字段
    )
    app.mount("/static", StaticFiles(directory=STATIC), name="static")
    app.include_router(user_router, tags=['user'], prefix='/api/v1')
    @app.on_event("startup")
    async def startup_db_client():
        print("mongodb已创建链接")
        app.mongodb_client = client
    @app.on_event("shutdown")
    async def shutdown_db_client():
        print("mongodb关闭链接")
        app.mongodb_client.close()
    @app.middleware("http") # request中间件
    async def log_requests(request, call_next):
        idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        logger.info(f"rid={idem} start request path={request.url.path}")
        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)
        logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
        return response
    return app
