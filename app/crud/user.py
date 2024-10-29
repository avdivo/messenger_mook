from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User, pwd_context


async def create_user(db: AsyncSession, username: str, password: str):
    """
    Создание пользователя
    :param db:
    :param username:
    :param password:
    :return:
    """
    result = await db.execute(select(User).where(User.username == username))
    db_user = result.scalars().first()  # Получаем первый результат
    if not db_user:
        hashed_password = pwd_context.hash(password)
        db_user = User(username=username, hashed_password=hashed_password)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
    else:
        raise ValueError("Пользователь с таким именем уже существует")

    return db_user


async def authenticate_user(db: AsyncSession, username: str, password: str):
    """
    Аутентификация пользователя
    :param db:
    :param username:
    :param password:
    :return:
    """
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()  # Получаем первый результат без использования await
    if user and user.verify_password(password):
        return user
    return None


async def get_all_users(db: AsyncSession):
    """
    Получение всех пользователей
    :param db:
    :return:
    """
    result = await db.execute(select(User))
    users = result.scalars().all()  # Получаем все результаты
    return users