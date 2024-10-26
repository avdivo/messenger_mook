from fastapi import FastAPI
from app.api.v1 import auth, websocket
from app.core.db import engine
from app.models.user import Base  # Импортируем Base из модели пользователя

app = FastAPI()

# Подключение маршрутов авторизации и WebSocket
app.include_router(auth.router, prefix="/api/v1")
app.include_router(websocket.router, prefix="/ws")


# Создание всех таблиц при запуске приложения (если они не существуют)
@app.on_event("startup")
def startup():
    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)
