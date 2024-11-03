from aiogram import types
from sqlalchemy.ext.asyncio import AsyncSession
from app.session.session_manager import get_session_user
from app.user.crud import change_tg_id


async def start_command(message: types.Message, db: AsyncSession):
    """
    Обрабатывает команду `/start` и связывает пользователя с проектом по одноразовому токену.

    :param message: сообщение пользователя
    :param db: сессия базы данных

    :return: None
    """
    text = message.text
    if " " not in text:
        await message.reply("Для регистрации необходим токен. Перейдите по представленной вам ссылке.")
    token = text.split(" ", 1)[1]  # Извлекаем токен после пробела
    user = await get_session_user(token)  # Получаем пользователя по токену (сессии)
    if not user:
        await message.reply("Неверный или истекший токен. Пожалуйста, попробуйте снова.")
        return

    # Связываем пользователя с проектом
    await change_tg_id(db, user.id, message.from_user.id)
    await message.reply("Вы успешно связали свой аккаунт с проектом.")


async def help_command(message: types.Message):
    """Обработка команды /help"""
    help_text = """
    Доступные команды:
    /start - Начать работу с ботом (требуется токен)
    /help - Показать это сообщение

    Я сообщу Вам о новом сообщении в сервисе обмена сообщениями, если вы будете не в сети.
    """
    await message.reply(help_text)
