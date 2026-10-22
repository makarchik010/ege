import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.db import init_db
from handlers.lessons import router as lessons_router

# Фейковый веб-сервер для бесплатного тарифа Render
async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def start_dummy_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render передает системный порт через переменную окружения PORT
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Fake web-server started on port {port}")

async def main():
    await init_db()
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(lessons_router)
    
    # Запускаем пинг-сервер фоном
    await start_dummy_server()
    
    print("🚀 Бот успешно стартовал!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
