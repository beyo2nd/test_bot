from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import select

from .models import async_session
from .models import User, Registered

#Запросы в базу данных

#добавляем всех юзеров, которые запустили бота

async def set_user(tg_id):
    print(f'set_user {tg_id}')
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            print("adding to users")
            session.add(User(tg_id=tg_id))
            await session.commit()

#добавляем все данные пользователя в бд

async def add_user(tg_id, name, surname, email, phone_number, birth_date):
    async with async_session() as session:
        new_user = Registered(
            tg_id=tg_id,
            name=name,
            surname=surname,
            email=email,
            phone_number=phone_number,
            birth_date=birth_date,
            InQueue=True
        )
        session.add(new_user)
        await session.commit()

#забираем данные пользователей, если Они ещё в очереди (InQueue = True)

async def get_inqueue_user():
    async with async_session() as session:
        result = await session.execute(select(Registered).where(Registered.InQueue == True).limit(1))
        user = result.scalars().first()
        return user
    
#Выставляет InQueue в значение False

async def set_inqueue_false(id: int):
    async with async_session() as session:
        result = await session.execute(select(Registered).where(Registered.id == id))
        user = result.scalars().first()
        
        if user:
            user.InQueue = False
            await session.commit()
            print(f"User with id {id} updated: InQueue set to False")
        else:
            print(f"No user found with id {id}")
        