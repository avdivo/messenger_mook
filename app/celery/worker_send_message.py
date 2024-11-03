import asyncio
from app.config.config import celery_app
from app.bot.config import bot

# Создаем глобальный цикл событий
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


@celery_app.task
def send_message_tg(username: str, tg_id: int):
    """Отправка оповещения о новом сообщении на Telegram
    :param username: имя пользователя который отправил сообщение
    :param tg_id: id получателя в Telegram
    """

    message = f"У вас новое сообщение от пользователя: {username}"

    # Создаем новый цикл событий для запуска асинхронной задачи
    loop.run_until_complete(bot.send_message(chat_id=tg_id, text=message))
