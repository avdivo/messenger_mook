from sqlalchemy import Column, Integer, String, BigInteger
from passlib.context import CryptContext
from app.config.db import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    """
    Модель пользователя для таблицы пользователей
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Идентификатор
    username = Column(String, unique=True, index=True)  # Имя пользователя
    hashed_password = Column(String)  # Хешированный пароль
    tg_id = Column(BigInteger, unique=True, index=True, nullable=True, default=0)  # id пользователя Телеграм

    def verify_password(self, password: str):
        """
        Проверка пароля
        :param password:
        :return:
        """
        return pwd_context.verify(password, self.hashed_password)
