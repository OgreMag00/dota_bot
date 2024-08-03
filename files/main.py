import asyncio
from aiogram import Bot, Dispatcher
from app import handlers
from app.database.models import async_main
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
# получаем токен
token_bot = TOKEN

# Объект бота
bot = Bot(token=token_bot)
# Диспетчер
dp = Dispatcher()


# Запуск процесса поллинга новых апдейтов
async def main():
    await async_main()  # подключаемся к базе
    dp.include_router(handlers.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())