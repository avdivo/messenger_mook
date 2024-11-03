import os
import redis
from celery import Celery

# URL базы данных PostgreSQL
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")
# Временно используем SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

# Настройки Celery
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=['app.celery.worker_send_message'],
    broker_connection_retry_on_startup=True,
)

# Настройки Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Подключение к Redis
redis_client = redis.asyncio.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=False)
