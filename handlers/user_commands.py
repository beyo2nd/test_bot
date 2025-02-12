import asyncio

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart

from keyboards import inline
from keyboards import reply

from database import requests as rq


router = Router()
#Стартовая команда (/start)Если пользователя нет в базе данных, то записываем его при старте.

@router.message(CommandStart())
async def start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(f"Привет, {message.from_user.first_name}! Это бот для заполнения обратной связи за человека.",
                         reply_markup= inline.start)
    
    
    