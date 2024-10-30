from app.config.config import celery_app
from app.config.config import redis_client
from app.websocket.websocket_manager import manager
from app.crud.user import get_user_by_id


@celery_app.task
def send_buffered_messages(user_id: str):
    """Отправка не отправленных сообщений для пользователя через WebSocket
    :param user: пользователь
    """
    messages = redis_client.lrange(f"messages:{user_id}", 0, -1)
    redis_client.delete(f"messages:{user_id}")  # Очищаем буфер после отправки

    user = get_user_by_id(user_id)

    # Отправка сообщений
    for message in messages:
        message = message.decode("utf-8")
        manager.send_personal_message(message, user)  # Отправка сообщения
