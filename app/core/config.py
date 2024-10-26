import os

# URL базы данных PostgreSQL
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")
# Временно используем SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Настройки Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
