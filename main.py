import asyncio
import logging
from environs import Env


from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


from handlers import router

async def main():
    env = Env()
    env.read_env()
    token = env('BOT_TOKEN')
    bot = Bot(token=token)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

    