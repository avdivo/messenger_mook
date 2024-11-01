from fastapi import FastAPI
from app.api.v1 import auth
from app.websocket import websocket
from app.config.db import engine
from app.models.user import Base  # Импортируем Base из модели пользователя

app = FastAPI()

# Подключение маршрутов авторизации и WebSocket
app.include_router(auth.router, prefix="/api/v1")
app.include_router(websocket.router, prefix="/ws")


# Создание всех таблиц при запуске приложения (если они не существуют)
# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
