from fastapi import FastAPI
from app.routers.router import init_app
from app.config.db import client
import uvicorn
def init():
    return init_app(FastAPI())


app = init()

@app.on_event("startup")
async def startup_db_client():
    print("mongodb已创建链接")
    app.mongodb_client = client

@app.on_event("shutdown")
async def shutdown_db_client():
    print("mongodb关闭链接")
    app.mongodb_client.close()

if __name__ == '__main__':
    uvicorn.run("main:app",reload=True)
