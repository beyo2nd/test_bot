import asyncio
from aiogram import Bot, Dispatcher

from handlers import bot_messages, user_commands, questionaries
from database.models import async_main
from config_reader import config
from database import requests as rq

dp = Dispatcher()


async def main():
    await async_main()
    bot = Bot(config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.include_routers(
        user_commands.router,
        questionaries.router,
        bot_messages.router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())