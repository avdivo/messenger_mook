import json
from app.history.crud import save_message
from app.user.crud import get_all_users
from sqlalchemy.ext.asyncio import AsyncSession
from app.websocket.websocket_manager import manager
from app.models.user import User
from app.websocket.buffered_messages import save_buffered_message


async def type_update(db: AsyncSession):
    """Подготовка сообщения для всех пользователей со
    списком пользователей и их статусом в системе.
    Формируем список пользователей и их статусов формируя словарь
    {
        "type": "update",
        "list": [
            {
                "user_id": "user_id",
                "username": "username",
                "status": "online/offline"
            },
            ...
        ]
    }
В списке list пользователи сортируются по статусу (сначала подключенные).
    """
    users = await get_all_users(db)  # Получаем список всех пользователей из БД
    list_online_users = await manager.connected_users_id()  # Получаем список пользователей онлайн

    users_list_online = []  # Список пользователей онлайн
    users_list_offline = []  # Список пользователей оффлайн
    for user in users:
        item = {"user_id": user.id, "username": user.username}
        if user.id in list_online_users:
            item["status"] = "online"
            users_list_online.append(item)
        else:
            item["status"] = "offline"
            users_list_offline.append(item)
    users_list_online.extend(users_list_offline)

    # Отправка сообщения всем пользователям
    await manager.broadcast(json.dumps({"type": "update", "list": users_list_online}))


async def type_message(db: AsyncSession, from_user: User, to_user: User, message: str):
    """Подготовка, отправление и сохранение сообщения.
    {
        "type": "message",
        "from": "username",
        "message": "text"
    }
    :param db: сессия базы данных
    :param from_user: отправитель
    :param to_user: получатель
    :param message: текст сообщения
    """
    # Сохранение сообщения в истории
    await save_message(db, from_user, to_user, message)

    # Формирование сообщения
    message = json.dumps({"type": "message", "from": from_user.username, "message": message})

    print('------------------------------------')
    print(to_user.id)

    # Отправка сообщения получателю
    if await manager.is_online(to_user):
        await manager.send_personal_message(message, to_user)  # Отправка сообщения
    else:
        await manager.send_personal_message("Пользователь не в сети", from_user)
        await save_buffered_message(to_user, message)  # Сохранение сообщения в буфер

    await db.commit()