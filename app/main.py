from fastapi import FastAPI
from app.api.v1 import auth, websocket

app = FastAPI()

# Подключение маршрутов авторизации и WebSocket
app.include_router(auth.router, prefix="/api/v1")
app.include_router(websocket.router, prefix="/ws")
