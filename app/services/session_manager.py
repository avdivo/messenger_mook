import redis
import uuid
from app.core.config import REDIS_HOST, REDIS_PORT

# Подключение к Redis
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)


def create_session(user_id: int):
    """
    Создание сессии
    :param user_id:
    :return: session_id
    """
    session_id = str(uuid.uuid4())  # Генерация уникального идентификатора сессии
    redis_client.set(session_id, user_id, ex=1800)  # TTL сессии - 30 минут
    return session_id


def get_session_user(session_id: str):
    """
    Получение ID пользователя по session_id
    :param session_id:
    :return: user_id
    """
    return redis_client.get(session_id)


# Удаление сессии
def delete_session(session_id: str):
    """
    Удаление сессии
    :param session_id:
    :return:
    """
    redis_client.delete(session_id)
