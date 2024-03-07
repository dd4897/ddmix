from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config.config import STATIC
from app.api.user import router as user_router


def init_app(app: FastAPI()):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 允许的域名列表
        allow_credentials=True,  # 允许在跨域请求中使用凭证（如Cookie）
        allow_methods=["*"],  # 允许的请求方法列表，这里使用通配符表示支持所有方法
        allow_headers=["*"],  # 允许的请求头列表，这里使用通配符表示支持所有头部字段
    )
    app.mount("/static", StaticFiles(directory=STATIC), name="static")
    app.include_router(user_router, tags=['user'], prefix='/api/v1/user')


    return app
