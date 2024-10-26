from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        """Инициализация менеджера подключений
        """
        self.active_connections: dict[int, WebSocket] = {}  # user_id: websocket

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        """Создание подключения
        """
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        """Закрытие подключения
        """
        if user_id in self.active_connections:
            self.active_connections.pop(user_id)

    async def send_personal_message(self, message: str, to_id: int):
        """Отправка персонального сообщения
        """
        await self.active_connections[to_id].send_text(f"{message}")

    async def broadcast(self, message: str):
        """Отправка сообщения всем
        """
        for connection in self.active_connections.values():
            await connection.send_text(message)


manager = ConnectionManager()
