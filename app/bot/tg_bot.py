from aiogram import Bot, Dispatcher
from aiogram.utils.executor import start_webhook
from .config import TELEGRAM_TOKEN, WEBHOOK_URL
from .handlers import register_user

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Регистрация обработчика команды `/start`
dp.register_message_handler(register_user, commands=["start"])


async def on_startup(dp):
    """
    Устанавливает вебхук при запуске бота.

    :param dp: диспетчер бота
    :return: None
    """
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    """
    Удаляет вебхук при завершении работы бота.

    :param dp: диспетчер бота
    :return: None
    """
    await bot.delete_webhook()


def start_bot():
    """
    Запускает Telegram-бот с использованием вебхука.

    :return: None
    """
    start_webhook(
        dispatcher=dp,
        webhook_path='/webhook',
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host='0.0.0.0',
        port=8443,
    )
