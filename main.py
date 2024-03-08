from fastapi import FastAPI
from app.routers.router import init_app
import uvicorn
def init():
    return init_app(FastAPI())


app = init()



if __name__ == '__main__':
    uvicorn.run("main:app",reload=True)
