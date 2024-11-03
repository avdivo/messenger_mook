from fastapi import FastAPI
from app.api.v1 import endpoints
from app.websocket import websocket
from app.bot.config import WEBHOOK_URL, bot

app = FastAPI()

# Подключение маршрутов авторизации и WebSocket
app.include_router(endpoints.router, prefix="/api/v1")
app.include_router(websocket.router, prefix="/ws")


@app.on_event("startup")
async def on_startup():
    """Установка вебхука при запуске приложения"""
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(WEBHOOK_URL)

