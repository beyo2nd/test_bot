import asyncio

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandObject, CommandStart
from keyboards import reply

router = Router()
