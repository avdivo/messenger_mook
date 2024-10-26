import redis
import uuid
import json
from app.core.config import REDIS_HOST, REDIS_PORT
from app.models.user import User

# Подключение к Redis
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)


def create_session(user: User):
    """
    Создание сессии
    :param user (object):
    :return: session_id
    """
    data = {
        "name": user.username,
        "user_id": user.id
    }
    session_id = str(uuid.uuid4())  # Генерация уникального идентификатора сессии
    redis_client.set(session_id, json.dumps(data), ex=1800)  # TTL сессии - 30 минут
    # docker run -d --name redis_container -p 6379:6379 redis
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
