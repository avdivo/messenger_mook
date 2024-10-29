from app.models.user import User
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        """Инициализация менеджера подключений
        """
        self.active_connections: dict[int, WebSocket] = {}  # user_id: websocket

    async def connect(self, user: User, websocket: WebSocket):
        await websocket.accept()
        """Создание подключения
        """
        self.active_connections[user.id] = websocket

    async def disconnect(self, user: User):
        """Закрытие подключения
        """
        if user.id in self.active_connections:
            await self.active_connections[user.id].close(code=1008)  # Разорвать соединение
            self.active_connections.pop(user.id)

    async def send_personal_message(self, message: str, to: User):
        """Отправка персонального сообщения
        """
        await self.active_connections[to.id].send_text(f"{message}")

    async def broadcast(self, message: str):
        """Отправка сообщения всем
        """
        for connection in self.active_connections.values():
            await connection.send_text(message)

    async def connected_users_id(self):
        """Получение списка id подключенных пользователей
        """
        return self.active_connections.keys()

manager = ConnectionManager()
