import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.websocket_manager import manager
from app.session.session_manager import get_session_user
from app.config.db import get_db
from app.websocket.messages import type_update, type_message
from app.user.crud import get_user_by_id
from app.websocket.buffered_messages import send_buffered_messages

router = APIRouter()


@router.websocket("/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    user = await get_session_user(session_id)
    if not user:
        print(f"Пользователь с сессией {session_id} не найден.")
        await websocket.close(code=1008)
        return

    # Создание сессии через get_db() для каждого подключения
    async for db in get_db():

        await manager.connect(user, websocket)  # Подключение пользователя
        await type_update(db)  # Отправка сообщения всем пользователям

        # Отправки буферизированных сообщений пользователю
        await send_buffered_messages(user)

        try:
            while True:
                data = await websocket.receive_text()  # Получение сообщения от пользователя

                try:
                    # Попытка парсинга сообщения как JSON
                    message = json.loads(data)

                    if message["type"] == "message":
                        # Отправка сообщения
                        # Принимаемое, пример: {"type": "message", "to": "2" , "message": "Это тебе сообщение!"}
                        to_user = await get_user_by_id(db, message["to"])  # Получение пользователя по id
                        if not to_user:
                            await manager.send_personal_message("Пользователь не найден", user)
                            continue
                        # Отправка сообщения
                        await type_message(db, user, to_user, message["message"])
                        continue

                except json.JSONDecodeError:
                    # Обработка ошибки в случае, если сообщение не является JSON
                    await websocket.send_text("Ошибка: Неверный формат сообщения")

        except WebSocketDisconnect:
            await manager.disconnect(user)
            await manager.broadcast(f"Пользователь {user.username} покинул чат.")
