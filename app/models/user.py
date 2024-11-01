from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
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

    def verify_password(self, password: str):
        """
        Проверка пароля
        :param password:
        :return:
        """
        return pwd_context.verify(password, self.hashed_password)


class Message(Base):
    """
    Модель сообщения для хранения переписки между пользователями
    """
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)  # Уникальный идентификатор сообщения
    chat_key = Column(String, index=True)  # Уникальный ключ для идентификации чата (пара пользователей)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Отправитель
    receiver_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Получатель
    content = Column(String, nullable=False)  # Содержание сообщения
    timestamp = Column(DateTime(timezone=True), server_default=func.now())  # Время отправки сообщения
    is_read = Column(Boolean, default=False)  # Прочитано ли сообщение

    def __init__(self, sender_id, receiver_id, content):
        """
        Конструктор модели сообщения. Автоматически генерирует chat_key из sender_id и receiver_id.
        """
        # Упорядочиваем id для создания уникального chat_key для каждой пары пользователей
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.chat_key = self.generate_chat_key(sender_id, receiver_id)
        self.content = content

    @staticmethod
    def generate_chat_key(user1_id, user2_id):
        """
        Генерирует уникальный chat_key, основанный на id двух пользователей.
        """
        sorted_ids = sorted([user1_id, user2_id])
        return f"{sorted_ids[0]}_{sorted_ids[1]}"
