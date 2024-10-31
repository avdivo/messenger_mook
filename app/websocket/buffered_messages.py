from app.config.config import redis_client
from app.websocket.websocket_manager import manager
from app.models.user import User


async def save_buffered_message(user: User, message: str):
    """Сохранение сообщения в Redis для пользователя
    :param user: пользователь
    :param message: сообщение
    """
    await redis_client.rpush(f"messages:{user.id}", message)


async def send_buffered_messages(user: User):
    """Отправка не отправленных сообщений для пользователя через WebSocket
    :param user: пользователь
    """
    messages = await redis_client.lrange(f"messages:{user.id}", 0, -1)
    await redis_client.delete(f"messages:{user.id}")  # Очищаем буфер после отправки

    # Отправка сообщений
    for message in messages:
        message = message.decode("utf-8")
        await manager.send_personal_message(message, user)  # Отправка сообщения
