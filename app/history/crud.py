from sqlalchemy.ext.asyncio import AsyncSession
from app.models.history import History
from app.models.user import User


async def save_message(db: AsyncSession, from_user: User, to_user: User, message: str):
    """
    Сохранение сообщения в истории
    :param db:  Сессия базы данных
    :param from_user:  Отправитель
    :param to_user:  Получатель
    :param message:  Текст сообщения
    :return:  Сохраненное сообщение
    """
    db_message = History(from_user.id, to_user.id, message)
    db.add(db_message)

    # Тут коммит не нужен, чтобы не истекали объекты
    # await db.commit()
    # await db.refresh(db_message)
    # return db_message
