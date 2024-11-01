from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.db import get_db
from app.user.crud import create_user, authenticate_user
from app.session.session_manager import create_session, delete_session, get_session_user
from app.websocket.websocket_manager import manager

router = APIRouter()  # Создание маршрутизатора


@router.post("/register")
async def register(username: str, password: str, db: AsyncSession = Depends(get_db)):
    """
    Регистрация пользователя
    :param Имя пользователя:
    :param Пароль:
    :param db:
    :return: идентификатор сессии
    """
    try:
        await create_user(db, username, password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Автоматический вход перенаправление на login
    return await login(username=username, password=password, db=db)


@router.post("/login")
async def login(username: str, password: str, db: AsyncSession = Depends(get_db)):
    """
    Вход в систему
    :param username:
    :param password:
    :param db:
    :return:
    """
    user = await authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    session_id = await create_session(user)  # Создание сессии
    return {"session_id": session_id}  # Возвращаем идентификатор сессии


@router.post("/logout")
async def logout(session_id: str):
    """
    Выход из системы
    :param session_id:
    :return: сообщение о выходе
    """
    user = await get_session_user(session_id)
    if not user:
        raise HTTPException(status_code=401, detail="Сессия не найдена")

    await manager.disconnect(user)  # Закрытие подключения
    await delete_session(session_id)  # Удаление сессии
    return {"message": "Вы вышли из системы"}
