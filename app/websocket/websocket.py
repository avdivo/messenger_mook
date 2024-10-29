from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.websocket_manager import manager
from app.services.session_manager import get_session_user
from app.config.db import get_db
from app.websocket.messages import type_update

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

        await manager.connect(user, websocket)
        print(await type_update(db))
        await manager.broadcast(await type_update(db))

        try:
            while True:
                data = await websocket.receive_text()
                await manager.broadcast(f"Пользователь {user.username}: {data}")
        except WebSocketDisconnect:
            manager.disconnect(websocket)
            await manager.broadcast(f"Пользователь {user.username} покинул чат.")
