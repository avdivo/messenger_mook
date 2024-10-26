from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from app.services.websocket_manager import manager
from app.services.session_manager import get_session_user

router = APIRouter()


@router.websocket("/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    user_id = get_session_user(session_id)

    if not user_id:
        await websocket.close(code=1008)
        return

    await manager.connect(websocket)
    await manager.broadcast(f"Пользователь {user_id} подключился к чату.")

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Пользователь {user_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Пользователь {user_id} покинул чат.")
