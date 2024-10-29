import redis
import uuid
import pickle
from app.config.config import REDIS_HOST, REDIS_PORT
from app.models.user import User

# Подключение к Redis
redis_client = redis.asyncio.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=False)


async def create_session(user: User):
    """
    Создание сессии
    :param user (object):
    :return: session_id
    """
    data_user = pickle.dumps(user)  # Сериализация объекта пользователя
    session_id = str(uuid.uuid4())  # Генерация уникального идентификатора сессии
    await redis_client.set(session_id, data_user, ex=1800)  # TTL сессии - 30 минут
    # docker run -d --name redis_container -p 6379:6379 redis
    # sudo docker start redis_container
    # sudo docker exec -it redis_container redis-cli
    return session_id


async def get_session_user(session_id: str):
    """
    Получение ID пользователя по session_id
    :param session_id:
    :return: user (object)
    """
    data_user = await redis_client.get(session_id)
    if data_user:
        return pickle.loads(data_user)  # Десериализация объекта пользователя
    return None


# Удаление сессии session_id
async def delete_session(session_id: str):
    """
    Удаление сессии
    :param session_id:
    :return:
    """
    await redis_client.delete(session_id)
