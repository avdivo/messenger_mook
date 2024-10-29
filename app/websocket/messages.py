import json
from app.crud.user import get_all_users
from sqlalchemy.ext.asyncio import AsyncSession
from app.websocket.websocket_manager import manager


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

    return json.dumps({"type": "update", "list": users_list_online})
