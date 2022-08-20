from fastapi import FastAPI
from app.router import route


def create_app():
    app = FastAPI()
    app.include_router(route)
    return app