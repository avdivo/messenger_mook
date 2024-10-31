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
        :param user: пользователь
        :param websocket: веб-сокет
        """
        self.active_connections[user.id] = websocket

    async def disconnect(self, user: User):
        """Закрытие подключения
        :param user: пользователь
        """
        if user.id in self.active_connections:
            try:
                await self.active_connections[user.id].close(code=1008)  # Разорвать соединение
            except RuntimeError as e:
                pass
            self.active_connections.pop(user.id)

    async def send_personal_message(self, message: str, to: User):
        """Отправка персонального сообщения
        :param message: сообщение
        :param to: получатель
        """
        await self.active_connections[to.id].send_text(f"{message}")

    async def broadcast(self, message: str):
        """Отправка сообщения всем
        :param message: сообщение
        """
        for connection in self.active_connections.values():
            await connection.send_text(message)

    async def connected_users_id(self):
        """Получение списка id подключенных пользователей
        :return: список id пользователей
        """
        return self.active_connections.keys()

    async def is_online(self, user: User):
        """Проверка пользователя онлайн
        :param user: пользователь
        :return: True/False
        """
        return user.id in self.active_connections

manager = ConnectionManager()
