import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.db import init_db
from handlers.lessons import router as lessons_router

async def main():
    await init_db()
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(lessons_router)
    
    print("🚀 Бот успешно стартовал!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
