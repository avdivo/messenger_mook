from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.crud.user import create_user, authenticate_user
from app.services.session_manager import create_session, delete_session

router = APIRouter()  # Создание маршрутизатора


@router.post("/register")
async def register(username: str, password: str, db: Session = Depends(get_db)):
    """
    Регистрация пользователя
    :param Имя пользователя:
    :param Пароль:
    :param db:
    :return: идентификатор сессии
    """
    try:
        create_user(db, username, password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Автоматический вход перенаправление на login
    return await login(response=None, username=username, password=password, db=db)


@router.post("/login")
async def login(response: Response, username: str, password: str, db: Session = Depends(get_db)):
    """
    Вход в систему
    :param response:
    :param username:
    :param password:
    :param db:
    :return:
    """
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    session_id = await create_session(user)  # Создание сессии
    return {"session_id": session_id}  # Возвращаем идентификатор сессии


@router.post("/logout")
async def logout(response: Response, request: Request):
    """
    Выход из системы
    :param response:
    :param request:
    :return: сообщение о выходе
    """
    session_id = request.cookies.get("session_id")
    if session_id:
        delete_session(session_id)  # Удаление сессии
    return {"message": "Вы вышли из системы"}
