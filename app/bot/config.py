import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from app.bot.handlers import start_command, help_command

# Загрузка переменных окружения из файла .env
load_dotenv()

# Токен Telegram-бота
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
# URL для вебхука
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
# Имя бота
BOT_USERNAME = os.getenv("BOT_USERNAME")

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
router = Router()
dp = Dispatcher(bot=bot)
dp.include_router(router)

# Регистрация обработчика команды `/start`
router.message.register(start_command, Command(commands=['start']))
# Регистрация обработчика команды `/help`
router.message.register(help_command, Command(commands=['help']))
