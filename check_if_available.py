#Скрипт для записи данных в форму
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import select

import aiohttp
import asyncio
from datetime import datetime

from database.models import async_session
from database.models import User, Registered

async def check_website(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                if response.status == 200:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Сайт доступен")
                else:
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Сайт недоступен, HTTP статус: {response.status}")
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Сайт недоступен: {e}")

async def main():
    url_to_check = "https://facebook.com"
    while True:
        await check_website(url_to_check)
        await asyncio.sleep(600)  # Задержка в 10 минут (600 секунд)